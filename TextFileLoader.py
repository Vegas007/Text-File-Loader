#! /usr/bin/env python
__name__ = "TextFileLoader"
__author__ = "VegaS"
__date__ = "2019-10-31"
__version__ = "0.0.3"

import os

#################################################
## Builtin translations
#################################################
TRANSLATE_DICT = {
	"LOAD_INVALID_FILE": "The file {} doesn't exists in your path!",
	"LOAD_INVALID_GROUP_SIZE": "Invalid group syntax!",
	"LOAD_INVALID_LIST_SIZE": "Invalid list syntax!",
	"LOAD_INVALID_TOKEN_SIZE": "LoadGroup : must have a value (filename: {} line: {} key: {})!",
	"LOAD_GET_TOKEN_LIST": "GetTokenList - Failed to find the key {} [{}:{}]!",

	"NODE_EMPTY": "Node to access has not set!",
	"NODE_CANNOT_FIND": "Node index to set is too large to access!",
	"NODE_NO_PARENT": "Current group node is already top!",
}

for localeName, localeValue in TRANSLATE_DICT.items():
	locals().update({localeName: localeValue})


#################################################
## Builtin functions
#################################################
USING_METIN2_CLIENT = False
if USING_METIN2_CLIENT:
	import app, dbg

	TraceFormat = lambda arg: dbg.TraceError(arg)
	IsExistFile = lambda arg: app.IsExistFile(arg)
else:
	TraceFormat = lambda arg: print(arg)
	IsExistFile = lambda arg: os.path.exists(arg)

NPOS = -1


#################################################
## Struct class
#################################################
class Struct():
	TPOSITION_SIZE = 3
	TQUATERNION_SIZE = 4
	TCOLOR_SIZE = 4

	class TPosition:
		def __init__(self, args):
			"""
			Define major axes (XYZ) intersect.

			:param x: The axis that goes side to side.
			:param y: The up to down position.
			:param z: The forward to backward position.
			"""
			self.x, self.y, self.z = args

	class TQuaternion:
		def __init__(self, args):
			""" Define data structure used to provide access to matrix and vector coordinates with the dot notation. """
			self.x, self.y, self.z, self.w = args

	class TColor:
		def __init__(self, args):
			"""
			Define colors using the red-green-blue-alpha (RGBA) model.
			
			:param r: Defines the intensity of red as an integer between 0 and 255, or as a percentage value between 0% and 100%.
			:param g: Defines the intensity of green as an integer between 0 and 255, or as a percentage value between 0% and 100%.
			:param b: Defines the intensity of blue as an integer between 0 and 255, or as a percentage value between 0% and 100%.
			:param a: Defines the opacity as a number between 0.0 (fully transparent) and 1.0 (fully opaque).
			:param args: A tuple which initialize the members.
			"""
			self.r, self.g, self.b, self.a = args


#################################################
## GroupNode
#################################################
class GroupNode:
	def __init__(self):
		"""
		:param groupName: The group name of node, string object.
		:param parentNode: The parent node of node, GroupNode class object.
		:param localTokenDict: The token dictionary where're stored all tokens, dict object.
		:param childNodeList: The child node list where're stored all of groups/lists with their parents, list of GroupNode objects.
		"""
		self.groupName = ''
		self.parentNode = None
		self.localTokenDict = {}
		self.childNodeList = []

	def __del__(self):
		del self.groupName
		del self.parentNode
		del self.localTokenDict
		del self.childNodeList

	def IsToken(self, tokenName):
		""" Returns a bool object, check if the token name exists inside of the dictionary. """
		return tokenName in self.localTokenDict

	def SetToken(self, tokenName, tokenValue):
		""" Insert in dictionary a new token name and his value, the parameter of tokenValue can be a string or a list of strings. """
		self.localTokenDict.update({tokenName: tokenValue})

	def SetChildNode(self, nodeObject):
		""" Append a new GroupNode class object to child node list. """
		self.childNodeList.append(nodeObject)

	def SetGroupName(self, name):
		""" Set current group name to specific name. """
		self.groupName = name

	def SetParent(self, parent):
		""" Set current parent of node with another parent, the parameter is a GroupNode object class. """
		self.parentNode = parent

	def GetToken(self, tokenName):
		""" Returns string or list of strings, of specific token name existing in dictionary, otherwise, it returns “None”. """
		return self.localTokenDict.get(tokenName, None)

	def GetChildNodeCount(self):
		""" Returns an int object, with the size of child node list. """
		return len(self.childNodeList)

	def GetChildNode(self, nodeIndex):
		""" Returns a GroupNode class object from the child node list by a specific index. """
		return self.childNodeList[nodeIndex]

	def GetTokenDict(self):
		""" Returns a dict object with all of the tokens (name, value) stored. """
		return self.localTokenDict

	def GetChildNodeList(self):
		""" Returns a list object with all nodes, each node is a class with structs and different parents, their parents also have another classes and so on. """
		return self.childNodeList

	def GetGroupName(self):
		""" Returns a string object of the group name. """
		return self.groupName

	def GetParent(self):
		""" Returns a string object of the parent node, GroupNode class object. """
		return self.parentNode

	def GetProxyParent(self):
		""" Returns a proxy to object which uses a weak reference. """
		return self


#################################################
## FileLoader
#################################################
class FileLoader:
	DELIMITER_STRIP = " \t\r\n"
	DELIMITER_TAB = ' \t'
	
	DELIMITER_COMMENT_START = '#'
	DELIMITER_COMMENT_END = "#--#"
	
	DELIMITER_START_STRING = '"'
	DELIMITER_END_STRING = "\""

	def __init__(self):
		"""
		param: fileLoaderList: The file loader list where's stored all of the converted lines from specific file.
		"""
		self.fileLoaderList = []

	def __del__(self):
		del self.fileLoaderList

	def Bind(self, lines):
		""" Insert the stripped lines into a list. """
		for line in lines:
			self.fileLoaderList.append(line.strip(self.DELIMITER_STRIP))

	def find_first_not_of(self, src, search, pos=0):
		"""
		Find absence of character in string

		Searches the string for the first character that does not
		match any of the characters specified in its arguments.
		When pos is specified, the search only includes characters
		at or after position pos, ignoring any possible occurrences
		before that character.

		Returns the position of the first character that does not match,
		if no such characters are found, the function returns npos.
		"""
		for i in range(pos, len(src)):
			if src[i] not in search:
				return i
		return NPOS

	def find_first_of(self, src, search, pos=0):
		"""
		Find character in string
		
		Searches the string for the first character that
		matches any of the characters specified in its arguments.
		When pos is specified, the search only includes characters at
		or after position pos, ignoring any possible occurrences before pos.

		Returns the position of the first character that matches,
		if no matches are found, the function returns npos.
		"""
		for i in range(pos, len(src)):
			if src[i] in search:
				return i
		return NPOS

	def substr(self, src, pos, baseCount):
		""" Generate substring
		Returns a newly constructed string object with its value
		initialized to a copy of a substring of this object.
		The substring is the portion of the object that starts at
		character position pos and spans len characters (or until the end of the string, whichever comes first).

		Returns a string object with a substring of this object.
		"""
		if baseCount > len(src) or baseCount == len(src):
			return str()
		elif baseCount <= NPOS:
			return src[pos: len(src)]
		return src[pos: pos + baseCount]

	def SplitLine(self, index):
		""" Returns a list object with the stripped lines and converted/checked to specific methods and delimiters if the conditions are acquired, otherwise, it returns “None”. """
		tokenString = self.GetLineString(index)
		tokenList = []
		basePos = 0

		while basePos < len(tokenString):
			beginPos = self.find_first_not_of(tokenString, self.DELIMITER_TAB, basePos)
			if beginPos == NPOS:
				return None

			if tokenString[beginPos] == self.DELIMITER_COMMENT_START and tokenString[beginPos: len(self.DELIMITER_COMMENT_END)] == self.DELIMITER_COMMENT_END:
				return None

			if tokenString[beginPos] == self.DELIMITER_START_STRING:
				beginPos += 1

				endPos = self.find_first_of(tokenString, self.DELIMITER_END_STRING, beginPos)
				if endPos == NPOS:
					return None

				basePos = endPos + 1
			else:
				endPos = self.find_first_of(tokenString, self.DELIMITER_TAB, beginPos)
				basePos = endPos

			tokenList.append(self.substr(tokenString, beginPos, endPos - beginPos))
			if self.find_first_not_of(tokenString, self.DELIMITER_TAB, basePos) == NPOS:
				break

		return tokenList

	def GetLineString(self, index):
		""" Returns a string line from list if the position matches or None. """
		if index >= self.GetLineCount():
			return None
		return self.fileLoaderList[index]

	def GetLineCount(self):
		""" Returns the length of the list. """
		return len(self.fileLoaderList)


#################################################
## TextFileLoader
#################################################
class TextFileLoader:
	BRACKET_START = '{'
	BRACKET_END = '}'

	TOKEN_TYPE_GROUP = "Group"
	TOKEN_TYPE_LIST = "List"

	TOKEN_TYPE = 0
	TOKEN_VALUE = 1
	TOKEN_LIMIT = 2

	def __init__(self):
		"""
		It's called when an object is created from the class and it allow the class to initialize the attributes of a class.

		:param m_curLineIndex: Current line index where is incremented while reading the file.
		:param m_TokensDict: All of the tokens (groups, lists, others) stored for dump to json later. <TODO>
		:param m_FileName: The file name which need to open for reading the data.
		:param m_fileLoader: The class parser for data.
		:param m_globalNode : The global node which is used as reference later.
		:param m_curNode: The current node which is set by reference or by SetChildNode.
		"""
		self.m_curLineIndex = 0
		self.m_tokensDict = {}

		self.m_fileName = ""
		self.m_fileLoader = FileLoader()

		self.m_globalNode = GroupNode()
		self.m_globalNode.SetGroupName('global')
		self.m_globalNode.SetParent(None)

		self.m_curNode = None

	def __del__(self):
		del self.m_curNode
		del self.m_globalNode
		del self.m_fileLoader
		del self.m_tokensDict

	def Load(self, c_szFileName):
		"""
			Loading data and bind a specific file.
		:returns
			A bool object depending of LoadGroup function which can be a recursive function called too, multiple times.
			False if path doesn't refers to an existing path or broken symbolic links.
			On some platforms, this function may return False if permission is not granted to execute os.stat() on the requested file, even if the path physically exists.
		"""
		if not IsExistFile(c_szFileName):
			TraceFormat(LOAD_INVALID_FILE.format(c_szFileName))
			return False

		self.m_fileName = c_szFileName

		file = open(c_szFileName, 'r')
		file_data = file.readlines()
		file.close()

		self.m_fileLoader.Bind(file_data)
		return self.LoadGroup(self.m_globalNode)

	def LoadGroup(self, groupNode, isRecursive=False):
		"""
			Load a specific group recursive or non-recursive.
			At first call the load group is a non-recursive function, sending the globalNode reference class as argument, then
			if inside of the text exists groups or lists, an recursive function LoadGroup will be called again, but this time
			with the 'pointer concept' as new class with specific parents and nodes.
		"""
		while self.m_curLineIndex < self.m_fileLoader.GetLineCount():
			tokenList = self.m_fileLoader.SplitLine(self.m_curLineIndex)
			if not tokenList:
				self.m_curLineIndex += 1
				continue

			if tokenList[self.TOKEN_TYPE][0] == self.BRACKET_START:
				self.m_curLineIndex += 1
				continue

			if tokenList[self.TOKEN_TYPE][0] == self.BRACKET_END:
				break

			## Group method
			if tokenList[self.TOKEN_TYPE] == self.TOKEN_TYPE_GROUP:
				if len(tokenList) != self.TOKEN_LIMIT:
					TraceFormat(LOAD_INVALID_GROUP_SIZE)
					return False

				group_parent_name = groupNode.GetGroupName()
				group_name = tokenList[self.TOKEN_VALUE]

				newGroupNode = GroupNode()
				newGroupNode.SetParent(groupNode)
				newGroupNode.SetGroupName(group_name)
				groupNode.SetChildNode(newGroupNode)

				self.m_curLineIndex += 1
				if not self.LoadGroup(newGroupNode, True):
					return False

			## List method
			elif tokenList[self.TOKEN_TYPE] == self.TOKEN_TYPE_LIST:
				if len(tokenList) != self.TOKEN_LIMIT:
					TraceFormat(LOAD_INVALID_LIST_SIZE)
					return False

				self.m_curLineIndex += 1
				while self.m_curLineIndex < self.m_fileLoader.GetLineCount():
					subTokenList = self.m_fileLoader.SplitLine(self.m_curLineIndex)
					if not subTokenList:
						self.m_curLineIndex += 1
						continue

					tokenLocalName = tokenList[self.TOKEN_VALUE]
					del tokenList[:]

					if subTokenList[self.TOKEN_TYPE][0] == self.BRACKET_START:
						self.m_curLineIndex += 1
						continue

					if subTokenList[self.TOKEN_TYPE][0] == self.BRACKET_END:
						break

					for subToken in subTokenList:
						tokenList.append(subToken)

					groupNode.SetToken(tokenLocalName, tokenList)
					self.m_curLineIndex += 1

			## Token method
			else:
				if len(tokenList) == 1:
					TraceFormat(LOAD_INVALID_TOKEN_SIZE.format(self.GetFileName(), self.m_curLineIndex, tokenList[self.TOKEN_TYPE]))
					return False

				groupNode.SetToken(*tokenList)

			self.m_curLineIndex += 1
		return True

	def SetTop(self):
		""" Set the current node as top by global node reference class. """
		self.m_curNode = self.m_globalNode

	def IsToken(self, tokenName):
		""" Returns a bool object depending of IsToken conditions while checking if the specific token name exists inside of the current node dictionary values, otherwise, it returns “False”. """
		if not self.m_curNode:
			TraceFormat(NODE_EMPTY)
			return False

		return self.m_curNode.IsToken(tokenName)

	def FindGroupName(self, nodeName, isParent=False):
		""" TODO: Find group by node name. """
		if not self.m_curNode:
			TraceFormat(NODE_EMPTY)
			return False

		if self.m_curNode.GetGroupName() == nodeName:
			return 0

		for nodeIndex, node in enumerate(self.m_curNode.GetChildNodeList()):
			if node.GetGroupName() == nodeName:
				return nodeIndex, NPOS

			if isParent:
				if node.GetParent():
					for parentNodeIndex, parentNode in enumerate(node.GetParent().GetChildNodeList()):
						if parentNode.GetGroupName() == nodeName:
							return nodeIndex, parentNodeIndex

					if node.GetParent().GetGroupName() == nodeName:
						return nodeIndex, NPOS
		return NPOS

	def SetChildNode(self, nodeName):
		""" Returns true and set the current node to found node, by name from current node list, if the current node has set and the node name exists in child node list, otherwise, it returns “False”. """
		if not self.m_curNode:
			TraceFormat(NODE_EMPTY)
			return False

		for node in self.m_curNode.GetChildNodeList():
			if node.GetGroupName() == nodeName:
				self.m_curNode = node
				return True

		return False

	def SetChildNodeFormat(self, c_rstrKeyHead, nodeIndex):
		""" Returns a bool object depending of SetChildNode conditions while sending a node name converted to string + index. """
		nodeName = "{:s}{:02d}".format(c_rstrKeyHead, nodeIndex)
		return self.SetChildNode(nodeName)

	def SetChildNodeIndex(self, nodeIndex):
		""" Returns true and set the current node to specific node from node list by index, if the current node has set and index is lower than length of the node list, otherwise, it returns “False”. """
		if not self.m_curNode:
			TraceFormat(NODE_EMPTY)
			return False

		if nodeIndex > self.m_curNode.GetChildNodeCount():
			TraceFormat(NODE_CANNOT_FIND)
			return False

		self.m_curNode = self.m_curNode.GetChildNode(nodeIndex)
		return True

	def SetParentNode(self):
		""" Returns true and set the current node to his parent, if the current node has set a parent, otherwise, it returns “False”. """
		if not self.m_curNode:
			TraceFormat(NODE_CANNOT_FIND)
			return False

		if not self.m_curNode.GetParent():
			TraceFormat(NODE_NO_PARENT)
			return False

		self.m_curNode = self.m_curNode.GetParent()
		return True

	def GetChildNodeCount(self):
		""" Returns an int object of the current node count, if the current node has set, otherwise, it returns “False”. """
		if not self.m_curNode:
			TraceFormat(NODE_EMPTY)
			return 0

		return self.m_curNode.GetChildNodeCount()

	def GetCurrentNodeName(self):
		""" Returns a string object of the current group name, if the current node has set a parent, otherwise, it returns “False”. """
		if not self.m_curNode or not self.m_curNode.GetParent():
			return "global"
		return self.m_curNode.GetGroupName()

	def GetTokenList(self, tokenName, tokenList, tokenSize=None):
		""" Returns true and send the reference of the token list, if the token name match, otherwise, it returns “False”. """
		if not self.IsToken(tokenName):
			TraceFormat(LOAD_GET_TOKEN_LIST.format(self.GetFileName(), self.m_curNode.GetGroupName(), tokenName))
			return False

		tokenValue = self.m_curNode.GetToken(tokenName)
		if not tokenValue:
			return False

		if isinstance(tokenValue, (tuple, list)):
			for item in tokenValue:
				tokenList.append(item)
		else:
			tokenList.append(tokenValue)

		if tokenSize:
			if len(tokenList) != tokenSize:
				return False

		return True

	def GetTokenValue(self, tokenName, tokenDataType=None, tokenSize=None):
		""" Returns a specific object, if the token name match and token list returned from reference function isn't empty, otherwise, it returns “False”. """

		def isfloat(token):
			if token.isalpha():
				return False
			try:
				float(token)
				return True
			except ValueError:
				return False

		tokenList = []
		if not self.GetTokenList(tokenName, tokenList, tokenSize) or not tokenList:
			return False

		tokenValue = tokenList[0]
		if tokenSize:
			tokenValue = tokenList[:tokenSize]

		tokenConditions = {
			float: isfloat(tokenValue),
			int: tokenValue.isdigit(),
			str: True,
			bool: True,
			Struct.TPosition: True,
			Struct.TQuaternion: True,
			Struct.TColor: True,
		}

		for dataType, hasAcquired in tokenConditions.items():
			if dataType == tokenDataType:
				if hasAcquired:
					return dataType(tokenValue)

		return False

	def GetTokenFloat(self, tokenName):
		""" Returns a float object from specific value, if the token name match and the value is floating data type, otherwise, it returns “False”. """
		return self.GetTokenValue(tokenName, float)

	def GetTokenInteger(self, tokenName):
		""" Returns an int object from specific value, if the token name match and the value contain digit numbers, otherwise, it returns “False”. """
		return self.GetTokenValue(tokenName, int)

	def GetTokenString(self, tokenName):
		""" Returns a string object from specific value, if the token name match, otherwise, it returns “False”. """
		return self.GetTokenValue(tokenName, str)

	def GetTokenBool(self, tokenName):
		""" Returns a bool object from specific value, if the token name match, otherwise, it returns “False”. """
		return self.GetTokenValue(tokenName, bool)

	def GetTokenPosition(self, tokenName):
		""" Returns a class object with members (x, y, z), if the token name match and the size of reference list is equal with TPOSITION_SIZE, otherwise, it returns “False”. """
		return self.GetTokenValue(tokenName, Struct.TPosition, Struct.TPOSITION_SIZE)

	def GetTokenQuaternion(self, tokenName):
		""" Returns a class object with members (x, y, z, w), if the token name match and the size of reference list is equal with TQUATERNION_SIZE, otherwise, it returns “False”. """
		return self.GetTokenValue(tokenName, Struct.TQuaternion, Struct.TQUATERNION_SIZE)

	def GetTokenColor(self, tokenName):
		""" Returns a class object with members (r, g, b, a), if the token name match and the size of reference list is equal with TCOLOR_SIZE, otherwise, it returns “False”. """
		return self.GetTokenValue(tokenName, Struct.TColor, Struct.TCOLOR_SIZE)

	def GetFileName(self):
		""" Returns a string object as file name which is in read mode. """
		return self.m_fileName

	def GetJSON(self):
		""" TODO: Convert all of the tokens into a dictionary and dump it to json.
			return json.dumps(self.m_tokensDict)
		"""
		pass


if __name__ == "__main__":
	def LoadFileTest(c_szFileName):
		# from TextFileLoader import TextFileLoader
		loader = TextFileLoader()
		if not loader.Load(c_szFileName):
			TraceFormat("Can't load the file: {}".format(c_szFileName))
			return

		# Set top
		loader.SetTop()

		# Reading from global node
		TraceFormat("Node name: {}, ANDROID_LINK: {}".format(loader.GetCurrentNodeName(), loader.GetTokenString("ANDROID_LINK")))
		TraceFormat("Node name: {}, IOS_LINK: {}".format(loader.GetCurrentNodeName(), loader.GetTokenString("IOS_LINK")))

		# Set the child node to Antutu_Benchmark_Android
		if not loader.SetChildNode("Antutu_Benchmark_Android"):
			TraceFormat("Syntax error: no Group Antutu_Benchmark_Android.")
			return

		# Reading from node Antutu_Benchmark_Android
		TraceFormat("Node name: {}, LAST_UPDATED: {}".format(loader.GetCurrentNodeName(), loader.GetTokenString("LAST_UPDATED")))

		# Reading the groups [Device00, Device01, Device02]
		for i in range(loader.GetChildNodeCount()):
			if not loader.SetChildNodeFormat("Device", i):
				TraceFormat("Syntax error: no Group Device{:02d}, node {}".format(i, loader.GetCurrentNodeName()))
				return

			for token in ("NAME", "RAM_AND_STORAGE", "CPU", "UX", "3D", "TOTAL_SCORE"):
				TraceFormat("Node name: {}, {}: {}".format(loader.GetCurrentNodeName(), token, loader.GetTokenString(token)))

			# Set the child node to his parent for can read the next group.
			loader.SetParentNode()

		# Set top
		loader.SetTop()
		TraceFormat("Node name: {}, DOWNLOAD_LINK: {}".format(loader.GetCurrentNodeName(), loader.GetTokenString("DOWNLOAD_LINK")))

	LoadFileTest('benchmark.txt')
