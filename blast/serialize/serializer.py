from ruamel.yaml import YAML
from blast.bit import Bit, BitMutable, BitImmutable, BitExpression, Reference
from blast.bitvector import BitVector


class BitIdentified(object):
    def __init__(self, bit: Bit, identifier: int, dependencies: list[int]):
        self.bit: Bit = bit
        self.identifier: int = identifier
        self.dependencies: list[int] = dependencies


class BitVectorSerializer(object):
    @staticmethod
    def encode_gate(gate: list[int]):
        """
        Encodes a gate of ints representing bits i.e. [0, 1, 1, 0] as a single integer.
        :param gate:
        :return:
        """
        value = 0
        for i in range(len(gate)):
            value <<= 1
            value |= gate[i]
        return value

    @staticmethod
    def _expressions_ordered(bit_vector: BitVector):
        """
        Returns a list of all expressions constituting each bit as well as the top level bit itself for each bit in the bit vector.
        The list is ordered such that each expression is only dependent on expressions that appear before it in the list.
        """
        expressions_seen: dict[Reference, int] = dict()
        expressions_ordered: list[BitIdentified] = list()

        def collect(expression: Bit):
            dependency_ids = []
            for dependency in expression.dependencies():
                if dependency not in expressions_seen:
                    dependency_id = collect(dependency.value)
                    dependency_ids.append(dependency_id)
                else:
                    dependency_id = expressions_seen[dependency]
                    dependency_ids.append(dependency_id)
            expression_id = len(expressions_seen)
            expressions_seen[Reference(expression)] = expression_id
            expressions_ordered.append(BitIdentified(expression, expression_id, dependency_ids))
            return expression_id

        expressions_bitvector = []
        for i in range(len(bit_vector)):
            top_id = collect(bit_vector.bit(i))
            expressions_bitvector.append(top_id)

        return expressions_ordered, expressions_bitvector

    @staticmethod
    def _serialize_identified_bit(bit_identified: BitIdentified) -> dict:
        bit_yaml = {
            'id': bit_identified.identifier
        }
        bit = bit_identified.bit
        if isinstance(bit, BitMutable):
            if bit.is_concrete():
                bit_yaml['value'] = int(bit)
            return bit_yaml
        if isinstance(bit, BitExpression):
            bit_yaml['gate'] = BitVectorSerializer.encode_gate(bit.gate)
            bit_yaml['dependencies'] = bit_identified.dependencies
            return bit_yaml
        if isinstance(bit, BitImmutable):
            bit_yaml['value'] = int(bit)
            return bit_yaml
        raise Exception(f"Bit implementation unknown to serializer: {type(bit)}")

    @staticmethod
    def serialize(bit_vector: BitVector, stream):
        """
        Writes a YAML representation of the bit vector to the given stream.
        :param bit_vector:
        :param stream:
        """
        expressions_ordered, top = BitVectorSerializer._expressions_ordered(bit_vector)
        bits = []
        for bit_identified in expressions_ordered:
            bits.append(BitVectorSerializer._serialize_identified_bit(bit_identified))
        top_ids = []
        for top_id in top:
            top_ids.append(top_id)
        data = {
            'bits': bits,
            'bitvector': top_ids
        }
        yaml = YAML()
        yaml.default_flow_style = None
        yaml.indent(mapping=2, sequence=4, offset=2)
        yaml.dump(data, stream)


class BitVectorDeserializer(object):
    @staticmethod
    def decode_gate(gate: int, input_bits: int):
        """
        Decodes a gate of given input bit length representing from its integer representation.
        :param gate:
        :param input_bits:
        :return:
        """
        value = []
        for i in range(input_bits ** 2):
            value.append(gate & 1)
            gate >>= 1
        return list(reversed(value))

    @staticmethod
    def _deserialize_identified_bit(bit_yaml: dict, bits_mapped: dict[int, Bit]) -> BitIdentified:
        """
        Deserializes a bit from its YAML representation.
        :param bit_yaml:
        :param bits_mapped: A map containing already decoded Bits by their identifier.
        """
        bit_id = bit_yaml['id']
        if 'value' in bit_yaml:
            bit = BitImmutable(bit_yaml['value'])
            return BitIdentified(bit, bit_id, [])
        if 'gate' in bit_yaml:
            input_bits = len(bit_yaml['dependencies'])
            gate_int = bit_yaml['gate']
            gate = BitVectorDeserializer.decode_gate(gate_int, input_bits)
            dependency_ids = bit_yaml['dependencies']
            dependencies = []
            for dependency_id in dependency_ids:
                dependencies.append(bits_mapped[dependency_id])
            bit = BitExpression(gate, *dependencies)
            return BitIdentified(bit, bit_id, dependency_ids)
        bit = BitMutable()
        return BitIdentified(bit, bit_id, [])

    @staticmethod
    def deserialize(stream) -> BitVector:
        """
        Reads a YAML representation of a bit vector from the given stream.
        """
        yaml = YAML()
        data = yaml.load(stream)
        bits_yaml = data['bits']
        bits_mapped = dict()
        for bit_yaml in bits_yaml:
            bit_identified = BitVectorDeserializer._deserialize_identified_bit(bit_yaml, bits_mapped)
            bits_mapped[bit_identified.identifier] = bit_identified.bit

        bitvector_yaml = data['bitvector']
        bitvector_len = len(bitvector_yaml)
        bitvector = BitVector.mutable(bitvector_len)
        for i in range(bitvector_len):
            bit_id = bitvector_yaml[i]
            bitvector[i] = bits_mapped[bit_id]
        return bitvector
