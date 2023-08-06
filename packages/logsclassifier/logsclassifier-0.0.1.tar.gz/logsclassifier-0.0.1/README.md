A binary classifier that takes as input a sentence and classifies if it is a log.

1. Parser - parses the text sentence to create a feature vector.
2. List of features:

    2.1 Contains date/time <br>
    2.2 Number of log levels: INFO | WARN | ERROR | DEBUG <br>
    2.3 Number of information on thread pool - eg [pool-3-thread-9] <br>
    2.4 Number Module/Component Name <br>
    2.5 Number of opening and closing brackets `[]` `{}`<br>
    2.6 Number of all CAPS words/tokens <br>
    2.7 Number of Camel Cased / Snake Cased words/tokens <br>
    2.8 Length of longest tokens <br>
