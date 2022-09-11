# Briareos
Algorithmic Trading System

Stored here are several scripts that constitute a complete Algorithmic Trading system, composed of several different modules capable of running in parallel.

This was my first coding project and I learned python while doing it, so don't expect great coding skills... at all.

The code is sparsely commented, i am very sorry for that and at least give a small description of the script at the very beginning.

The folder Main contains the main modules of the system. The file Module_Terminal.py is responsible for the execution of the modules of the algo-trading system. It assigns the execution of these modules to machines\computer in the network, allowing them to run in parallel. The system expect the presence of 4 machines in the network, counting with the one running this script. These in turn execute the files\modules in the subfolder MatlabPythonModules; which execute matlab code by the matlab-python api. The matlab files required by each module in MatlabPythonModules are, respectively divided by subfolders in the folder MatlabCode.
These modules are:
  - Database Modules : This modules scrape all required information from API's of several data providers
  - Optimization Module (TOptimization_Modules.py): This module is responsible for the optimization of the trading strategies used by the algorithm. It also optimizes parameters of the Predictions Module.
  - Predictions and Portfolio Management Module (Pred_PMModule.py): This module is responsible for predicting future market trends and optimize the portfolios considering those predictions
  - Trading Module (TradM_OEM.py): This module is responsible for generating and executing trading orders (Buy\sell). It guarantees the proper accounting of two separate portfolios that are in fact a single portfolio on an exchange (here binance). It also executes the scheduled withdrawal of part of the total funds on the Exchange.

The folder WarRoom contains scripts rquired to create an visualize Streamlit Dashboards to monitor all parts of the system. 

The system is very autonomous, requiring only the user to monitor problems with gathered information by the system and hardware. It manages erros\exceptions and reports any problems both in the Dashboards and by e-mail so as to be able to notify immediatly of problems detected.

The project took 3 years and suffered from performance problems (profitability), resulting in its abandonment. The cause of the problems is due to a naive approach to many stages of development and the use of mathematical tools not completly understood by me at the time. Overfitting and the use of more data than required plagued later stages of development. The constant pursue of remarkable results in backtesting not matched by the actual performance of the algorithm.

Still, presented here as a complete package that can be modified or scraped for parts as some are indeed of interest.
