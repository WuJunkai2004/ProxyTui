import sys

# 全局注册表，用于存储和管理所有的分发器对象
# 结构: {'函数名': <对应的PlatformDispatcher对象>}
_DISPATCHERS = {}


class PlatformDispatcher:
    """
    一个分发器对象。
    它表现得像一个函数，但其内部逻辑是根据当前操作系统
    调用已注册的特定平台函数。
    """
    def __init__(self, name):
        self._name = name
        self._registry = {}
        self._default_func = None # 存储默认/备用函数
        self._current_func = None # 当前使用的函数, 用于缓存
        self.__doc__ = "Platform-dependent function. Use help() on a specific implementation for details."

    def register(self, platform, func):
        """为特定平台注册一个函数实现。"""
        if platform == 'default':
            self._default_func = func
        else:
            self._registry[platform] = func

        if not self.__doc__ or self.__doc__.startswith("Platform-dependent"):
             self.__doc__ = func.__doc__


    def __call__(self, *args, **kwargs):
        """
        核心调用逻辑。当这个对象被当作函数调用时执行。
        """
        if self._current_func is not None:
            return self._current_func(*args, **kwargs)

        current_platform = sys.platform

        func = self._registry.get(current_platform)

        if func is None:
            for platform_key, registered_func in self._registry.items():
                if current_platform.startswith(platform_key):
                    func = registered_func
                    break

        if func is None:
            func = self._default_func

        if func is None:
            raise NotImplementedError(
                f"Function '{self._name}' is not implemented for platform '{current_platform}' or has no default."
            )
        
        self._current_func = func
        return func(*args, **kwargs)


class platform_specific:
    def __init__(self, platform):
        self.platform = platform

    def __call__(self, func):
        func_name = func.__name__

        if func_name not in _DISPATCHERS:
            _DISPATCHERS[func_name] = PlatformDispatcher(func_name)

        dispatcher:PlatformDispatcher = _DISPATCHERS[func_name]
        dispatcher.register(self.platform, func)

        return dispatcher


windows = platform_specific("win32")
linux   = platform_specific("linux")
macos   = platform_specific("darwin")
default = platform_specific("default")