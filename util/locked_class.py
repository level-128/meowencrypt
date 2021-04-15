def lock(cls):
	def new_init(self, *args, **kwargs):
		raise LockedContentError("you can't create another instance since it has already been created once")
	
	def new_getattr(*args):
		raise LockedContentError("you are not allowed to modify variables inside the instance.")
	
	cls.__init__ = new_init
	cls.__setattr__ = new_getattr
	del new_init
	del new_getattr


class LockedContentError(Exception):
	def __init__(self, *args):
		super().__init__(self, *args)
		
		
if __name__ == '__main__':
	raise Exception("this file is not used for execution.")
