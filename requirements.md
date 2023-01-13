# Software Requirements

## Vision

This app will predict the value of a given horse based on data gathered from the Zed Run website and display relevant data and prediction in results in an easy-to-digest dashboard. This currently requires manual analysis to determine if the horse is a good investment, so our app will solve this problem.

## Scope (In/Out)

IN:

* Allow users to query a specific horse
* Shows dashboard of the sales from that day
* Keep database of all horses sold in the last year (ID and sales price) and filter to compare against
* Output a valuation range of the input horse ID (median and range)

OUT:

* Will not be a web app (Jupyter notebook front end)
* NOT financial advice or recommendation of what to buy
* No string input in CLI (only integers)
* Complete interface, will only open Jupyter notebook

Minimum Viable Product:

* Given a horses ID, give a command line printout of the horse's valuation range 

## Stretch Goals

* Jupyter notebook with graphical display of horse's metrics and comparisons
* Back-end hosted online (Vercel)
* Jupyter notebook hosted on GitHub or Kaggle
* Allow the user to search by horse attributes


## Functional Requirements

* Need it to accept an input of a horse ID and output a valuation range 
* Need to save the sale data from all horses in the previous year to create comps/training data
* Need to create a valuation range via ML
* Output the valuation range to the user

## Data Flow

1. Build database of all sales data and attributes from previous year
  * Get sales and ID 
  * Get attributes of IDs 
  * Compile both into single database
2. Get attributes of input horse ID from API
3. Filter the data table based on characteristics of input horse and run regressions
4. Compare input horse to new dataset
5. Return result of comparison (valuation range)

## Non-Functional Requirements 

Usability

* Intuitive CLI structure
* Output valuation range is readable
* Stretch Goals - Jupyter notebook graphical representation is easy to understand and draw conclusions from

Testability

* Write tests that use sample IDs of known horses to ensure result is valid. 
* Tests to make sure pre-existing database is valid data.
