from test_graph import *


def run_all_tests():
    print('Запуск тестов')

    loader = unittest.TestLoader()
    suite = unittest.TestSuite()

    suite.addTest(loader.loadTestsFromTestCase(TestGraph))
    suite.addTest(loader.loadTestsFromTestCase(TestGraphIO))

    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)

    print(f"Тестов запущено: {result.testsRun}")
    print(f"Успешно: {result.testsRun - len(result.failures) - len(result.errors)}")
    print(f"Провалено: {len(result.failures)}")
    print(f"Ошибок: {len(result.errors)}")

    if result.failures:
        print("\nПроваленные тесты:")
        for test, traceback in result.failures:
            print(f"  ❌ {test}")

    if result.errors:
        print("\nТесты с ошибками:")
        for test, traceback in result.errors:
            print(f"  💥 {test}")

    return result.wasSuccessful()


if __name__ == '__main__':
    success = run_all_tests()
