class GlobalValue:

	dict={}

	def set(self,**keys):

		try:

			for key,value in keys.items():

				self.dict[key]=value

				print(self.dict.keys())

		except BaseException  as msg :

			raise msg

	def del_map(self, key):
		
		try:

			del self.dict[key]
			return self.dict
		except KeyError:
			print("key:'" + str(key) + "'  不存在")


	def get(self,key):

		try:

			return self.dict[key]

		except KeyError:

			return







