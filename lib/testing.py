from colorama import Fore, Style

from option_selection import OptionSelector


def test_bed(function, inputs, expected_outputs, tracer=None):
    """
    Run a test bed on the given inputs and expected outputs. Optionally, allow the user to run a trace on any failed
    test
    :param function: Function to test. This function should take a single argument
    :param inputs: Inputs upon which to test the function
    :param expected_outputs: Expected outputs for the corresponding inputs
    :param tracer: Trace to run for each failed test. This function should take 3 arguments; the list of inputs,
    the list of expected outputs, and the index of the failing test
    :return: List of failure indexes (these will be 1 less than the test numbers shown by the testbed)
    """
    failed: list[int] = []
    for i in range(len(inputs)):
        in_ = inputs[i]
        in_str = str(in_)
        exp = expected_outputs[i]
        out = function(in_)
        if out == exp:
            print(f'\n{Fore.GREEN}Passed test {i+1}:{Style.RESET_ALL}'
                  f'\n-------------------------------'
                  f'\nIn : {in_str}'
                  f'\nOut: {Fore.GREEN}{out}{Style.RESET_ALL}')
        else:
            failed.append(i)
            print(f'\n{Fore.RED}Failed test {i+1}:{Style.RESET_ALL}'
                  f'\n-------------------------------'
                  f'\nIn : {in_str}'
                  f'\nOut: {Fore.RED}{out}{Style.RESET_ALL}'
                  f'\nExp: {exp}')

    print(f'\nPassed {(total := len(inputs)) - (fails := len(failed))} of {total} tests.')

    if fails > 0 and tracer:
        print('You can view a trace for each failed test below:')
        selector = OptionSelector()
        for x in failed:
            selector.add_option(str(x + 1), f'Test {x + 1}', lambda: tracer(inputs, expected_outputs, x))
        selector.run()

    return failed
