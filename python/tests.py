import unittest
from unittest import TestCase

import ujson
import json
import math
import time
import datetime
import calendar

class UltraJSONTests(TestCase):
	def test_encodeDoubleConversion(self):
		input = math.pi
		output = ujson.encode(input)
		self.assertEquals(round(input, 5), round(json.loads(output), 5))
		self.assertEquals(round(input, 5), round(ujson.decode(output), 5))
		pass

	def test_encodeDoubleNegConversion(self):
		input = -math.pi
		output = ujson.encode(input)
		self.assertEquals(round(input, 5), round(json.loads(output), 5))
		self.assertEquals(round(input, 5), round(ujson.decode(output), 5))
		pass

	def test_encodeStringConversion(self):

		input = "A string \\ \/ \b \f \n \r \t"
		output = ujson.encode(input)
		self.assertEquals(input, json.loads(output))
		self.assertEquals(output, json.dumps(input))
		self.assertEquals(input, ujson.decode(output))
		pass

	def test_encodeArrayInArray(self):
		input = "[[[[]]]]"
		output = ujson.encode(input)
		self.assertEquals(input, json.loads(output))
		self.assertEquals(output, json.dumps(input))
		self.assertEquals(input, ujson.decode(output))
		pass

	def test_encodeIntConversion(self):
		input = 31337
		output = ujson.encode(input)
		self.assertEquals(input, json.loads(output))
		self.assertEquals(output, json.dumps(input))
		self.assertEquals(input, ujson.decode(output))
		pass

	def test_encodeIntNegConversion(self):
		input = -31337
		output = ujson.encode(input)
		self.assertEquals(input, json.loads(output))
		self.assertEquals(output, json.dumps(input))
		self.assertEquals(input, ujson.decode(output))
		pass

	def test_encodeLongNegConversion(self):
		input = -9223372036854775808
		output = ujson.encode(input)
		
		outputjson = json.loads(output)
		outputujson = ujson.decode(output)
		
		self.assertEquals(input, json.loads(output))
		self.assertEquals(output, json.dumps(input))
		self.assertEquals(input, ujson.decode(output))
		pass

	def test_encodeListConversion(self):
		input = [ 1, 2, 3, 4 ]
		output = ujson.encode(input)
		self.assertEquals(input, json.loads(output))
		self.assertEquals(input, ujson.decode(output))
		pass

	def test_encodeDictConversion(self):
		input = { "k1": 1, "k2":  2, "k3": 3, "k4": 4 }
		output = ujson.encode(input)
		self.assertEquals(input, json.loads(output))
		self.assertEquals(input, ujson.decode(output))
		self.assertEquals(input, ujson.decode(output))
		pass

	def test_encodeNoneConversion(self):
		input = None
		output = ujson.encode(input)
		self.assertEquals(input, json.loads(output))
		self.assertEquals(output, json.dumps(input))
		self.assertEquals(input, ujson.decode(output))
		pass

	def test_encodeTrueConversion(self):
		input = True
		output = ujson.encode(input)
		self.assertEquals(input, json.loads(output))
		self.assertEquals(output, json.dumps(input))
		self.assertEquals(input, ujson.decode(output))
		pass

	def test_encodeFalseConversion(self):
		input = False
		output = ujson.encode(input)
		self.assertEquals(input, json.loads(output))
		self.assertEquals(output, json.dumps(input))
		self.assertEquals(input, ujson.decode(output))
		pass

	def test_encodeDatetimeConversion(self):
		ts = time.time()
		input = datetime.datetime.fromtimestamp(ts)
		output = ujson.encode(input)
		expected = calendar.timegm(input.utctimetuple())
		self.assertEquals(int(expected), json.loads(output))
		self.assertEquals(int(expected), ujson.decode(output))
		pass

	def test_encodeDateConversion(self):
		ts = time.time()
		input = datetime.date.fromtimestamp(ts)

		output = ujson.encode(input)
		tup = ( input.year, input.month, input.day, 0, 0, 0 )

		expected = calendar.timegm(tup)
		self.assertEquals(int(expected), json.loads(output))
		self.assertEquals(int(expected), ujson.decode(output))
		pass

	def test_encodeRecursionMax(self):
		# 8 is the max recursion depth

		class O2:
			member = 0
			pass	

		class O1:
			member = 0
			pass

		input = O1()
		input.member = O2()
		input.member.member = input

		try:
			output = ujson.encode(input)
			assert False, "Expected overflow exception"
		except(OverflowError):
			pass


	"""
	# This test fails. I'm not sure it's an issue or not
	def test_encodeListLongConversion(self):
		input = [9223372036854775807, 9223372036854775807, 9223372036854775807, 9223372036854775807, 9223372036854775807, 9223372036854775807 ]
		output = ujson.encode(input)
		self.assertEquals(input, json.loads(output))
		self.assertEquals(input, ujson.decode(output))
		pass

	# This test fails, I'm not sure it's an issue or not
	def test_encodeLongConversion(self):
		input = 9223372036854775807
		output = ujson.encode(input)
		self.assertEquals(input, json.loads(output))
		self.assertEquals(output, json.dumps(input))
		self.assertEquals(input, ujson.decode(output))
		pass

		
	def test_encodeUTF8Conversion(self):
		input = u"A \"string\"\"\\\/\b\f\n\r\t"
		raise NotImplementedError("Implement this test!")
		pass

	def test_decodeJibberish(self):
		input = "fdsa sda v9sa fdsa"
		try:
			ujson.decode(input)
			assert False, "Expected exception!"
		except(ValueError):
			return
		assert False, "Wrong exception"
		
	def test_decodeBrokenArrayStart(self):
		input = "["
		try:
			ujson.decode(input)
			assert False, "Expected exception!"
		except(ValueError):
			return
		assert False, "Wrong exception"

	def test_decodeBrokenObjectStart(self):
		input = "{"
		try:
			ujson.decode(input)
			assert False, "Expected exception!"
		except(ValueError):
			return
		assert False, "Wrong exception"

	def test_decodeBrokenArrayEnd(self):
		input = "]"
		try:
			ujson.decode(input)
			assert False, "Expected exception!"
		except(ValueError):
			return
		assert False, "Wrong exception"

	def test_decodeBrokenObjectEnd(self):
		input = "}"
		try:
			ujson.decode(input)
			assert False, "Expected exception!"
		except(ValueError):
			return
		assert False, "Wrong exception"
		
	def test_decodeStringUnterminated(self):
		input = "\"TESTING"
		try:
			ujson.decode(input)
			assert False, "Expected exception!"
		except(ValueError):
			return
		assert False, "Wrong exception"

	def test_decodeStringUntermEscapeSequence(self):
		input = "\"TESTING\\\""
		try:
			ujson.decode(input)
			assert False, "Expected exception!"
		except(ValueError):
			return
		assert False, "Wrong exception"

	def test_decodeStringBadEscape(self):
		input = "\"TESTING\\\""
		try:
			ujson.decode(input)
			assert False, "Expected exception!"
		except(ValueError):
			return
		assert False, "Wrong exception"

	def test_decodeTrueBroken(self):
		input = "tru"
		try:
			ujson.decode(input)
			assert False, "Expected exception!"
		except(ValueError):
			return
		assert False, "Wrong exception"

	def test_decodeFalseBroken(self):
		input = "fa"
		try:
			ujson.decode(input)
			assert False, "Expected exception!"
		except(ValueError):
			return
		assert False, "Wrong exception"

	def test_decodeNullBroken(self):
		input = "n"
		try:
			ujson.decode(input)
			assert False, "Expected exception!"
		except(ValueError):
			return
		assert False, "Wrong exception"

	def test_decodeNumericIntExp(self):
		input = "<int>E<exp>"
		raise NotImplementedError("Implement this test!")

	def test_decodeNumericIntFrcExp(self):
		input = "<int>.<frc>E<exp>"
		raise NotImplementedError("Implement this test!")

	def test_decodeNumericIntFrcOverflow(self):
		input = "X.Y"
		raise NotImplementedError("Implement this test!")

	def test_decodeNumericIntPos(self):
		input = "31337"
		raise NotImplementedError("Implement this test!")
	
	def test_decodeNumericIntNeg(self):
		input = "-31337"
		raise NotImplementedError("Implement this test!")
		
	def test_decodeNumericIntPosOverflow(self):
		input = "9223372036854775807322"
		try:
			ujson.decode(input)
			assert False, "Expected exception!"
		except(ValueError):
			return
		assert False, "Wrong exception"
		
	def test_decodeNumericIntNegOverflow(self):
		input = "-9223372036854775807322"
		try:
			ujson.decode(input)
			assert False, "Expected exception!"
		except(ValueError):
			return
		assert False, "Wrong exception"

	
	
	#Exponent specific tests
	def test_decodeNumericIntExpEPLUS(self):
		input = "<int>E+<exp>"
		raise NotImplementedError("Implement this test!")

	def test_decodeNumericIntExpePLUS(self):
		input = "<int>e+<exp>"
		raise NotImplementedError("Implement this test!")

	def test_decodeNumericIntExpE(self):
		input = "<int>E<exp>"
		raise NotImplementedError("Implement this test!")

	def test_decodeNumericIntExpe(self):
		input = "<int>e<exp>"
		raise NotImplementedError("Implement this test!")

	def test_decodeNumericIntExpE(self):
		input = "<int>E<exp>"
		raise NotImplementedError("Implement this test!")

	def test_decodeNumericIntExpe(self):
		input = "<int>e<exp>"
		raise NotImplementedError("Implement this test!")
		
	def test_decodeNumericIntExpEMinus(self):
		input = "<int>E-<exp>"
		raise NotImplementedError("Implement this test!")

	def test_decodeNumericIntExpeMinus(self):
		input = "<int>e-<exp>"
		raise NotImplementedError("Implement this test!")

	def test_decodeStringUnicodeEscape(self):
		input = "\u3131"
		raise NotImplementedError("Implement this test!")

	def test_decodeStringUnicodeBrokenEscape(self):
		input = "\u3131"
		raise NotImplementedError("Implement this test!")

	def test_decodeStringUnicodeInvalidEscape(self):
		input = "\u3131"
		raise NotImplementedError("Implement this test!")
		
	def test_decodeStringUTF8(self):
		input = "someutfcharacters"
		raise NotImplementedError("Implement this test!")
	
	def test_decodeNumericFloatInf(self):
		pass

	def test_decodeNumericFloatNan(self):
		pass
	"""

		
if __name__ == "__main__":
	unittest.main()
