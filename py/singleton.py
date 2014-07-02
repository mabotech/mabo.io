


class Singleton(type):
  def __call__(cls, *args):
    if not hasattr(cls, 'instance'):
      cls.instance = super(Singleton, cls).__call__(*args)
    return cls.instance
