# Backend Engineering Challenge

Assumptions:

- tried to use a cost-effective solution for the problem at hand;

- research was also appropriately time-boxed;

- would have used a time series library like Pandas if performance was
  not a issue and we needed to greatly expand on the features;

- relying on Python's sorting algorithm; could come up with a more
  convoluted implementation(*) if we can't afford to use Python's
  "sorted".

Risks:

- not sure if there will be some accumulated numerical error, suppose
  not.

- uncertain about the extensibility of the code, but for the given
  scope, the architecture seems adequate.

Usage:

Just type ./moving_average.py for a description of the input arguments.

An usage example is:

./moving_average.py --input_file events.json --window_size 10

(*) Inserting mirror events in a sorted fashion (in the correct time
order).
