# Proposal

## Title

Analysis about Law Enforcement and Crime Rate Data of United States

## Group Members

- Haoyuan Han
- Lingxuan Ye
- Mingxiao Liu

## Overview

### Problem Statement

When people make decisions on where they live and work, the crime rate and safety level are always the crucial factors to be considered. Therefore, analyzing the crime rate data from where they live is the best way to help people understand their living and working environment and get familiar with how they can keep safe in their current locations. We pick the *Communities and Crime Data* provided by Micheal Redmond from La Salle University, Philadelphia, PA, 19141, USA. With the given dataset, we can analyze the violent crimes rate, law enforcement data of different cities to find out what city is safe enough to reside in.

### Data

#### Source

https://archive.ics.uci.edu/ml/datasets/Communities+and+Crime

#### Abstract

Communities within the United States. The data ombines socio-economic data from the 1990 US Census, law inforcement data from the 1990 US LEMAS survey, and crime data from the 1995 FBI UCR.

### User story

1. As an international student who accidentally time-travels to 1995, I need to pick a relatively safe city in the United States so that I can carry on my study life without any trouble.
2. As an unemployed poor guy, I need to find a city with the weakest law enforcement according to the only data I can get which could be outdated so that I can commit my perfect robbery crime.
3. As a researcher in 1995, I want to analyze crime data and provide it to the police so that the police can use my analysis results to strengthen police deployment in future in order to improve the local living environment.

## Design

1. In user story 1, the main idea is to find cities with the lowest crime rate and the most sufficiently funded and adequately staffed police department.
2. Contrary to the first story, we need to find cities with the weakest law enforcement in user story 2.
3. In user story 3, we need to find all the imbalanced crime rate and law enforcement.

In general, all three stories should apply geo data visualization for the given data in different cities to directly show the secure level.