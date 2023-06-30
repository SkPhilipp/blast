from ruamel.yaml import YAML
from blast.bit import Bit, BitMutable, BitImmutable, BitExpression, Reference
from blast.bitvector import BitVector


class BitIdentified(object):
    def __init__(self, bit: Bit, identifier: int, dependencies: list[int]):
        self.bit: Bit = bit
        self.identifier: int = identifier
        self.dependencies: list[int] = dependencies


class BitVectorSerializer(object):
    def __init__(self, bit_vector: BitVector):
        self.bit_vector = bit_vector

    def _expressions_ordered(self):
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
        for i in range(len(self.bit_vector)):
            top_id = collect(self.bit_vector.bit(i))
            expressions_bitvector.append(top_id)

        return expressions_ordered, expressions_bitvector

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

    def serialize(self, stream):
        """
        Writes a YAML representation of the bit vector to the given stream.
        """
        bits = []
        expressions_ordered, top = self._expressions_ordered()
        for bit_identified in expressions_ordered:
            bit = bit_identified.bit
            bit_yaml = {
                'id': bit_identified.identifier
            }
            if isinstance(bit, BitMutable):
                if bit.is_concrete():
                    bit_yaml['value'] = int(bit)
                bits.append(bit_yaml)
                continue
            if isinstance(bit, BitExpression):
                bit_yaml['gate'] = BitVectorSerializer.encode_gate(bit.gate)
                bit_yaml['dependencies'] = bit_identified.dependencies
                bits.append(bit_yaml)
                continue
            if isinstance(bit, BitImmutable):
                bit_yaml['value'] = int(bit)
                bits.append(bit_yaml)
                continue
            raise Exception(f"Bit implementation unknown to serializer: {type(bit)}")
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
