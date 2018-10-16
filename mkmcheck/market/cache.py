import typing as t

import threading
import sqlite3
import json
import os
from queue import Queue

from promise import Promise

from mkmcheck import paths


CACHE_DIR = os.path.join(paths.APP_DATA_DIR, 'cache')
DB_PATH = os.path.join(CACHE_DIR, 'cache.db')


class Retriever(threading.Thread):

	def __init__(self, path: str = DB_PATH):
		super().__init__(daemon = True)

		self._path = path

		self._connection = None #type: sqlite3.Connection
		self._cursor = None #type: sqlite3.Cursor

		self._task_queue = Queue()

		self._running_lock = threading.Lock()
		self._running = False

	@property
	def running(self) -> bool:
		with self._running_lock:
			return self._running

	def stop(self) -> None:
		with self._running_lock:
			if self._running:
				self._running = False

	def _select(self, request: str, resolve: t.Callable[[t.Any], t.Any]) -> None:
		selected_values = list(
			value[0]
			for value in
			self._cursor.execute(
				"SELECT value FROM entries WHERE request=?",
				(request,),
			)
		)

		resolve(
			selected_values
		)

	def _update(self, request: str, value: str, resolve: t.Callable[[t.Any], t.Any]) -> None:
		self._cursor.execute(
			"INSERT INTO entries VALUES (?, ?)",
			(request, value),
		)
		self._connection.commit()

		resolve(None)


	def _clear(self) -> None:
		self._cursor.execute(
			"DELETE FROM entries",
		)
		self._connection.commit()

	def clear(self) -> Promise:
		return Promise(lambda resolve, reject: self._task_queue.put((self._clear, ())))

	def select(self, request: str) -> Promise:
		return Promise(lambda resolve, reject: self._task_queue.put((self._select, (request, resolve))))

	def update(self, request: str, value: t.Any) -> Promise:
		return Promise(lambda resolve, reject: self._task_queue.put((self._update, (request, value, resolve))))

	def run(self) -> None:
		self._running = True
		self._connection = sqlite3.connect(self._path)
		self._cursor = self._connection.cursor()

		while True:
			with self._running_lock:
				if not self._running:
					break

			action, values = self._task_queue.get()
			action(*values)


class Cacher(object):

	@classmethod
	def _create_database(cls, path: str = DB_PATH):
		if not os.path.exists(CACHE_DIR):
			os.makedirs(CACHE_DIR)

		connection = sqlite3.connect(path)
		cursor = connection.cursor()

		cursor.execute("CREATE TABLE entries (request text, value text)")

		connection.commit()
		connection.close()

	def __init__(self, path: str = DB_PATH, retriever: t.Optional[Retriever] = None):
		if not os.path.exists(path):
			self._create_database(path)

		self._retriever = Retriever(path) if retriever is None else retriever

		if not self._retriever.running:
			self._retriever.start()

	def clear(self) -> Promise:
		return self._retriever.clear()

	def __call__(self, decorated: t.Callable[[str], t.Any]) -> t.Callable[[str], t.Any]:
		def _cache_wrapper(request: str) -> t.Any:
			cached = self._retriever.select(request).get()

			if not cached:
				value = decorated(request)
				self._retriever.update(request, json.dumps(value))

				return value

			return json.loads(cached[0])

		return _cache_wrapper

