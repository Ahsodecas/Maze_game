import unittest
from bfs import bfs, create_maze_from_draft, create_maze_map
from generator import maze_generator


class TestBfs(unittest.TestCase):
    def test_reachable_maze_bfs(self):
        maze_draft1 = [
            [1, 1, 1, 1, 1, 1, 1, 1],
            [1, 0, 0, 0, 0, 0, 0, 1],
            [1, 0, 1, 1, 1, 1, 0, 1],
            [1, 0, 1, 0, 0, 1, 0, 1],
            [1, 0, 1, 0, 0, 0, 0, 1],
            [1, 0, 0, 0, 0, 1, 0, 1],
            [1, 0, 0, 1, 0, 1, 0, 1],
            [1, 1, 1, 1, 1, 1, 1, 1]
        ]

        self.assertEqual(bfs(create_maze_map(), create_maze_from_draft(maze_draft1)), 10)

    def test_unreachable_maze_bfs(self):
        maze_draft2 = [
            [1, 1, 1, 1, 1, 1, 1, 1],
            [1, 0, 0, 0, 0, 0, 0, 1],
            [1, 1, 1, 1, 1, 1, 1, 1],
            [1, 0, 1, 0, 0, 1, 0, 1],
            [1, 0, 1, 0, 0, 0, 0, 1],
            [1, 0, 0, 0, 0, 1, 0, 1],
            [1, 0, 0, 1, 0, 1, 0, 1],
            [1, 1, 1, 1, 1, 1, 1, 1]
        ]

        self.assertEqual(bfs(create_maze_map(), create_maze_from_draft(maze_draft2)), -1)

    def test_empty_reachable_maze_bfs(self):
        maze_draft3 = [
            [0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0]
        ]

        self.assertNotEqual(bfs(create_maze_map(), create_maze_from_draft(maze_draft3)), -1)

    def test_generated_maze_is_doable(self):
        for _ in range(100):
            coordinates_of_walls = []
            maze_generator(create_maze_map(), coordinates_of_walls)
            self.assertNotEqual(bfs(create_maze_map(), coordinates_of_walls), -1)

    def test_correct_create_maze_map(self):
        maze_map = [[(0, 0), (64, 0), (128, 0), (192, 0), (256, 0), (320, 0), (384, 0), (448, 0)],
                       [(0, 64), (64, 64), (128, 64), (192, 64), (256, 64), (320, 64), (384, 64), (448, 64)],
                       [(0, 128), (64, 128), (128, 128), (192, 128), (256, 128), (320, 128), (384, 128), (448, 128)],
                       [(0, 192), (64, 192), (128, 192), (192, 192), (256, 192), (320, 192), (384, 192), (448, 192)],
                       [(0, 256), (64, 256), (128, 256), (192, 256), (256, 256), (320, 256), (384, 256), (448, 256)],
                       [(0, 320), (64, 320), (128, 320), (192, 320), (256, 320), (320, 320), (384, 320), (448, 320)],
                       [(0, 384), (64, 384), (128, 384), (192, 384), (256, 384), (320, 384), (384, 384), (448, 384)],
                       [(0, 448), (64, 448), (128, 448), (192, 448), (256, 448), (320, 448), (384, 448), (448, 448)]]
        self.assertEqual(maze_map, create_maze_map())


if __name__ == '__main__':
    unittest.main()
