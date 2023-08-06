""" Вспомогательные функции

"""

import multiprocessing as _M
import pathlib as pa
import time
import typing as _T


class SubProcessMixing(object):
    """ Миксин для инициализации доп процесса внутри класса """

    _started: bool

    _queue: _T.Optional[_M.Queue]
    _process: _T.Optional[_M.Process]

    def __init__(self) -> None:
        self._started = False

        self._queue = None
        self._process = None

    def start(self):
        if self._started:
            self.stop()

        self._queue = _M.Queue(-1)
        self._process = _M.Process(target=self.on_process)
        self._process.start()

        self._started = True

    def stop(self):
        self._queue.put(None)
        while not self._queue.empty():
            time.sleep(0.1)

        self._process.join()
        self._process.terminate()

        self._queue.close()
        self._queue.join_thread()

        self._started = False

    def __del__(self):
        if self._started:
            self.stop()


class FileIOProcess(SubProcessMixing):
    """ Класс, запускаемый в отдельном процессе, для записи чего-либо в файл """

    files: dict[str, _T.IO]
    counts: dict[str, int]

    def __init__(self) -> None:
        self.files = {}
        self.counts = {}

        super().__init__()

    def __file_create(self, stringPath: str):
        """ Создание файла и родительских папок

        Args:
            stringPath (str): Путь до файла

        """

        paPath = pa.Path(stringPath)

        if not paPath.parent.is_dir():
            paPath.parent.mkdir(parents=True)

        if not paPath.is_file():
            paPath.write_text('')

    def __file_close(self):
        """ Закрытие всех файлов """

        for _, fileIO in self.files.items():
            fileIO.close()

    def __file_write_on_step(self, path: str, string: str):
        """ Запись строки в файл с шагом в 50 записей """

        self.files[path].write(string)

        self.counts[path] += 1

        if self.counts[path] >= 50:
            self.files[path].close()
            self.files[path] = open(path, 'a')
            self.counts[path] = 0
    
    def __file_write(self, path: str, string: str):
        """ Запись строки в файл """

        self.files[path].write(string)
        self.files[path].close()
        self.files[path] = open(path, 'a')

    def __read_queue(self) -> _T.Generator[tuple[str, str], None, None]:
        while True:
            record = self._queue.get()

            if record is None:
                break

            (path, string) = record

            yield (path, string)

    def __check_file(self, path: str):
        """ 

        Args:
            path (str): [description]

        """

        if path not in self.files:
            self.__file_create(path)
            self.files[path] = open(path, 'a')
            self.counts[path] = 0

    def on_process(self):
        for path, string in self.__read_queue():
            self.__check_file(path)

            self.__file_write_on_step(path, string)
        self.__file_close()
    
    def __del__(self):
        for path, string in self.__read_queue():
            self.__check_file(path)

            self.__file_write(path, string)
        self.__file_close()

        super().__del__()
