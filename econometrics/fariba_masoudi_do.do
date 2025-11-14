*******************************************************
* DID Analysis - Medicaid Expansion and Uninsured Rate
* Author: Fariba Masoudi
* personal number: 9110096808

*******************************************************
clear


* STEP 1: Load dataset
use "D:\ECONOMETRICS\IV 09 APRIL\medicaid_did.dta", clear

* STEP 2: Create identifiers and treatment variables
* Generate numeric state ID for panel setup
encode state, gen(state_id)

* Create treatment group dummy
gen treated = ///
    state == "Arizona" | state == "Arkansas" | state == "California" | ///
    state == "Colorado" | state == "Connecticut" | state == "Delaware" | ///
    state == "Hawaii" | state == "Illinois" | state == "Iowa" | ///
    state == "Kentucky" | state == "Maryland" | state == "Massachusetts" | ///
    state == "Minnesota" | state == "Nevada" | state == "New Jersey" | ///
    state == "New Mexico" | state == "New York" | state == "North Dakota" | ///
    state == "Ohio" | state == "Oregon" | state == "Rhode Island" | ///
    state == "Vermont" | state == "Washington" | state == "West Virginia"

* Post-treatment indicator
gen post = year >= 2014

* DID interaction term
gen did = treated * post

* STEP 3: Set panel structure
xtset state_id year

* STEP 4: Summary stats
sum uninsured_rate treated post did

* STEP 5: Parallel trends graph
preserve
collapse (mean) uninsured_rate, by(year treated)
twoway (line uninsured_rate year if treated == 1, sort lcolor(blue)) ///
       (line uninsured_rate year if treated == 0, sort lcolor(red)), ///
       legend(label(1 "Treated States") label(2 "Control States")) ///
       title("Parallel Trends in Uninsured Rate") ///
       ytitle("Uninsured Rate (%)") xtitle("Year")
restore

* STEP 6: DID Regression (base model)
xtreg uninsured_rate i.treated##i.post, fe cluster(state_id)
estimates store did_base
esttab did_base using "did_base_results.rtf", se label replace ///
    title("DID Regression - Medicaid Expansion Impact on Uninsured Rate")

* STEP 7: Robustness - Add Year Fixed Effects
xtreg uninsured_rate i.treated##i.post i.year, fe cluster(state_id)
estimates store did_robust
esttab did_robust using "did_yearfe_results.rtf", se label replace ///
    title("DID with Year Fixed Effects")

* STEP 8: Event Study Setup
gen rel_year = year - 2014
gen rel_year_fe = .
replace rel_year_fe = rel_year if treated == 1
tab rel_year_fe, gen(rel_yr_)

* Keep treated group only for event study
preserve
keep if !missing(rel_year_fe)

* Omit rel_yr_6 (year -1) as base category
xtreg uninsured_rate rel_yr_1 rel_yr_2 rel_yr_3 rel_yr_4 rel_yr_5 ///
                    rel_yr_7 rel_yr_8 rel_yr_9 rel_yr_10 rel_yr_11 ///
                    rel_yr_12 rel_yr_13 rel_yr_14 rel_yr_15, fe cluster(state_id)

* Plot event study
ssc install coefplot, replace
coefplot, ///
    keep(rel_yr_*) drop(rel_yr_6) vertical ///
    xline(6, lpattern(dash)) ///
    ciopts(recast(rcap)) ///
    xlabel(1 "2008" 2 "2009" 3 "2010" 4 "2011" 5 "2012" 6 "2013" ///
           7 "2014" 8 "2015" 9 "2016" 10 "2017" 11 "2018" ///
           12 "2019" 13 "2020" 14 "2021" 15 "2022", angle(vertical)) ///
    xtitle("Year") ///
    ytitle("Change in Uninsured Rate (%)") ///
    title("Event Study: Impact of Medicaid Expansion") ///
    msymbol(circle)
restore

* STEP 9: Save final dataset (optional)
save "medicaid_final_panel.dta", replace
