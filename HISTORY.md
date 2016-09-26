# History

## 2016-09-26

 Working on identifying failed examples uniquely over the last N runs for a given branch. I am doing this in the "SpecMetrics-ProcessingFromAWS" notebook for now.

 The way I'm doing it is this:
 - over a subset of runs on `develop`, gather the example that failed the most often,
 - over the same subset of runs, find all examples that ran _before_ this example when it failed in the run (`all_before_most_failed_examples`),
 - count the occurrence of each unique example in `all_before_most_failed_examples` and find the most present ones: this is probably one of them that is causing issues in your most failed example!

 NB: instead of this approach which is doing an union on tests that ran before the most failed one, I should rather do an intersection!
