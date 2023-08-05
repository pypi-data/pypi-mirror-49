**function_profile decorator**

Provides decorator for time and memory profiling of functions.

Metrics:

* time - time for a single function call
* memory -  peak memory used by the function. The peak memory is the difference between the starting minimum value, and the highest value.


Usage:

.. code-block:: python

    from function_profile_decorator import profile

    @profile(time_prof=True, mem_prof=True)
    def factoriel_loop(n: int) -> int:
        """Calculate factoriel non-recursive."""
        fac: int = 1
        for i in range(1, n + 1):
            fac = fac * i
        return fac

    factoriel_loop(n=100)

Output:

    factoriel_loop(, n=100)

    Time   0.00001450

    Memory 0.0546875
