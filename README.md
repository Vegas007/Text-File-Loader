# Text File Loader
 A python tool that allow to read differents data type, ordered by groups, lists, parents and more.

How to use:
```python
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
```
