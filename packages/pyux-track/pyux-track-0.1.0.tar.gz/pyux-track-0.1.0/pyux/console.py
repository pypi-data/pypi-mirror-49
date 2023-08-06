
import shutil
import sys

from colorama import init, deinit
from colorama import Fore, Style

from pyux.errors import ColorValueError
from pyux.errors import StyleValueError


def _validate_iterable(iterable):
    """Return the argument if it is iterable, ``TypeError`` otherwise"""
    try:
        iter(iterable)
        return iterable
    except TypeError as e:
        raise TypeError("Argument is not iterable : %s" % repr(e))


class Wheel:
    """Print a wheel turning at the same speed as iterations

    This class decorates an iterable in a for loop by printing a turning wheel
    and the number of iterations. It can also be used manually within the loop
    rather than decorating the iterable.
    
    For loops on integers, you can give ``n`` rather than the iterable, which will
    be converted in ``range(n)``.

    :param iterable: (default ``None``) an iterable, or an integer for standard ``range(n)`` values
    :param print_value: Print iteration value instead of counter next to the wheel
    :type print_value: bool
    
    :return: A decorated iterable
    :raise: ``TypeError`` if ``iterable`` is not an iterable
    
    :Example:
    
    >>> for _ in Wheel(['a', 'b', 'c', 'd']):
    >>>     # this will print the number of iteration at each step next to the weel
    >>> for _ in Wheel(5):
    >>>     # idem
    >>> for letter in Wheel(['a', 'b', 'c', 'd'], print_value = True):
    >>>     # this whill print the letter next to the wheel instead
    >>>     # of the number of iterations
    
    """
    def __init__(self, iterable = None, print_value: bool = False):
        self.print_value = print_value
        iterable = [] if iterable is None else iterable
        if isinstance(iterable, float) or isinstance(iterable, int):
            iterable = range(int(iterable))
        self.iterable = _validate_iterable(iterable)
        self.last_message = None
        
    def __iter__(self):
        self.n = 0
        for element in self.iterable:
            yield element
            if self.print_value:
                self.print(step = self.n, message = element)
                self.last_message = element
            else:
                self.print(step = self.n)
                self.last_message = self.n + 1
            self.n += 1
        self.close(message = self.last_message)
        
    @staticmethod
    def print(step: int, message: str = None):
        """Print the position of the wheel for a given step and message"""
        message = step if message is None else message
        if step % 4 == 0:
            sys.stdout.write('\r - | %s' % message)
            sys.stdout.flush()
        elif step % 4 == 1:
            sys.stdout.write('\r \\ | %s' % message)
            sys.stdout.flush()
        elif step % 4 == 2:
            sys.stdout.write('\r | | %s' % message)
            sys.stdout.flush()
        elif step % 4 == 3:
            sys.stdout.write('\r / | %s' % message)
            sys.stdout.flush()
        return
    
    def close(self, message: str = None) -> None:
        """Print the wheel for the length of the iterable
        
        This method is called when the ``for`` loop from which ``Wheel`` was
        called ends, so that the last value printed is equal to the
        number of iterations.
        
        If a message is provided, it is printed rather than the length of the
        iterable.
        
        It can also be called manually when ``Wheel`` was instantiated outside
        of a ``for`` loop.
        
        :param message: (default ``None``) message to print next to wheel
        :type message: str
        
        :return: ``None``
        
        :Example:
        
        >>> wheel = Wheel(iterable = 'A string iterable')
        >>> wheel.close()
        >>> wheel.close(message = 'Overwriding length of iterable')
        
        """
        if message is not None:
            self.print(step = len(self.iterable), message = message)
        else:
            self.print(step = len(self.iterable))
        sys.stdout.write('\n')
        sys.stdout.flush()
        return
    

class ProgressBar:
    """Print progress bar with percent

    For each iteration, print first the percentage of progress, the number of iterations
    against the total number of iterations to do, and a progress bar.
    
    For loops on integers, you can give ``n`` rather than the iterable, which will
    be converted in ``range(n)``.
    
    The class can be instantiated outside of a ``for`` loop and be used manually.
    
    :param iterable: (default ``None``) an iterable, or an integer for standard ``range(n)`` values
    :param ascii_only: Use ascii character for progress bar
    :type: ascii_only: bool
    
    :return: A decorated iterable
    :raise: ``TypeError`` if ``iterable`` is not an iterable
    
    :Example:
    
    >>> from time import sleep
    >>> for _ in ProgressBar(3000, ascii_only = True):
    >>>     sleep(0.001)
    
    """
    def __init__(self, iterable = None, ascii_only: bool = False):
        iterable = [] if iterable is None else iterable
        if isinstance(iterable, float) or isinstance(iterable, int):
            iterable = range(int(iterable))
        self.iterable = _validate_iterable(iterable)
        self.bar_char = '=' if ascii_only else '\u2588'
        
        self.real_width = len(iterable)
        give_space = 4 + 3 + len(str(self.real_width))*2 + 1 + 3 + 2    # xxx% | step/total_step | ===... |
        self.bar_width = shutil.get_terminal_size()[0] - give_space
        self.real_step = self.real_width / self.bar_width
        
        self.current_console_step = 0
        
    def __repr__(self):
        str_values = (self.real_width, self.bar_width, self.current_console_step)
        return "ProgressBar(real_width = %d, bar_width = %d, current_console_step = %d)" % str_values
        
    def __iter__(self):
        self.n = 0
        for element in self.iterable:
            yield element
            self.print(step = self.n)
            self.n += 1
        self.close()
        
    def print(self, step: int) -> None:
        """Print progress bar for the current iteration"""
        if step >= self.current_console_step * self.real_step:
            str_values = (
                step * 100 / self.real_width,
                str(step).zfill(len(str(self.real_width))),
                self.real_width,
                self.bar_char * self.current_console_step
            )
            sys.stdout.write('\r%d%% | %s/%d | %s' % str_values)
            sys.stdout.flush()
            self.current_console_step += 1
        return
    
    def close(self) -> None:
        """Print bar with 100% completion

        When the for loop finished, print a last progress bar with 100%
        completion. Otherwise iteration index would end just before reaching 100%
        due to index starting from zero rather than one.
        
        Can be called manually when ``ProgressBar`` is used outside of a ``for``
        loop.

        :return: None
        
        :Example:
        
        >>> ProgressBar(iterable = 'A string iterable').close()
        
        """
        sys.stdout.write('\r100%% | %d/%d | ' % (self.real_width, self.real_width))
        sys.stdout.write(self.bar_char * self.bar_width + ' |\n')
        sys.stdout.flush()
        return


class ColourPen:
    """Util for writing colored and styled messages in console

    Available colors and styles can be found in ``ColourPen.__colors__``
    and ``ColourPen.__styles__``. Arguments are matched against these values.
    
    Only one instance is needed to print text with different styles. By default,
    styles and colours remains the same until changed or reset, allowing to
    write successive prints with the same format without having to specify it
    each time.
    
    :Example:
    
    >>> pen = ColourPen()
    >>> pen.write('A blue and bright message', color = 'cyan', style = 'bright')
    >>> pen.write('Still a blue message', reset = True, newline = True)
    >>> pen.write('That message is back to normal')
    >>> pen.close()
    
    """
    __colors__ = [
        'BLACK',
        'RED',
        'GREEN',
        'YELLOW',
        'BLUE',
        'MAGENTA',
        'CYAN',
        'WHITE',
        'RESET'
    ]
    __styles__ = [
        'DIM',
        'NORMAL',
        'BRIGHT',
        'RESET_ALL'
    ]
    
    def __init__(self):
        init()
        self.message = ''
    
    def __repr__(self):
        return "ColourPen(message = %s)" % self.message
    
    def _colourise(self, color = 'RESET'):
        """Colourise the message with the given color

        Color argument is checked against possible values and
        is case insensitive. Can be combined with style.
        
        :param color: (default ``'RESET'``) color to use. Giving ``None`` does
        nothing, which is, returns the message with the color from the
        previous call to ``write()``
        :type color: str
        
        :return: ``self``
        :raise: ``ColorValueError`` if the color does not exist
        """
        try:
            color = color.upper()
        except AttributeError:
            pass
        try:
            color_prefix = getattr(Fore, color)
        except TypeError:
            color_prefix = ''
        except AttributeError:
            raise ColorValueError("color must be one of %s" % repr(self.__colors__))
        self.message = color_prefix + self.message
        return self
    
    def _style(self, style = 'RESET_ALL'):
        """Style the message with the given style

        Style argument is checked against possible values and
        is case insensitive. Can be combined with colourise.
        
        :param style: (default ``'RESET_ALL'``) style to use. Giving ``None`` does
        nothing, which is, returns the message with the style from the
        previous call to ``write()``
        
        :return: ``self``
        :raise: ``StyleValueError`` if the style does not exist
        """
        try:
            style = style.upper()
        except AttributeError:
            pass
        try:
            style_prefix = getattr(Style, style)
        except TypeError:
            style_prefix = ''
        except AttributeError:
            raise StyleValueError("style must be one of %s" % repr(self.__styles__))
        self.message = style_prefix + self.message
        return self

    def write(self, message: str = '',
              color: str = None, style: str = None,
              flush: bool = True, newline: bool = False, reset: bool = False):
        """Write a colored and styled message
        
        The method returns ``self`` so that you can chain calls to the method
        from a single instance.
        
        :Example:
        
        >>> pen = ColourPen()
        >>> pen.write('Hello... ', color = 'cyan').write('Goodbye !', reset = True, newline = True)
        
        Default behavior is to pass on current style to subsequent calls, so you
        only need to style and colour once if you want to keep the same format. This
        is accomplished through ``None`` values for ``color`` and/or ``style``,
        which means that giving ``None`` does not ignore style and color !
        
        To remove style for the message to print, use ``style = 'RESET_ALL'``.
        To remove style after printing, use ``reset = True``
        
        Message is printed with ``sys.stdout.write()`` rather than ``print()``,
        allowing precise control over printing. Default behavior is to flush at
        each print and to keep the console cursor where it is.
        
        You can thus decide to "write" several messages and flush them at once,
        and you can add a newline after writing to mimic the behavior of ``print()``.
        
        :param message: (default ``''``) message to write
        :type message: str
        :param color: (default ``None``) colour to use, checked against possible values.
        :type color: str
        :param style: (default ``None``) style to use, checked against possible values
        :type style: str
        :param flush: flush console after writing message
        :type flush: bool
        :param newline: insert a new line after writing message
        :type newline: bool
        :param reset: reset style and colour after writing message
        :type reset: bool
        
        :return: ``self`` so as to be able the chain calls to ``write()``
        :raise: ``ColorValueError``
        :raise: ``StyleValueError``
        """
        self.message = message
        self._colourise(color = color)\
            ._style(style = style)
        sys.stdout.write(self.message)
        
        if reset:
            self.write(message = '', style = 'RESET_ALL', reset = False, newline = newline)
            return self
        if newline:
            self.write(message = '\n', newline = False, reset = reset)
            return self
        if flush:
            sys.stdout.flush()
        return self
        
    def close(self) -> None:
        """Reset all styles and close ``colorama`` util
        
        The method flushes an empty message with reset styles and a newline.
        Closing make the ``sys.stdout`` go back to normal : styling and colouring
        will not be recognised after it.
        
        :return: ``None``
        """
        self.write(message = '', flush = True, reset = True, newline = True)
        deinit()
        return
