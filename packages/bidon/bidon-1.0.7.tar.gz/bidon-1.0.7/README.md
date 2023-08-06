Bidon - Refreshing Data Handling
================================

Bidon, **noun**: a container for water or other liquids, particularly as used by cyclists. (French)

> "A bidon is a simple but indispensable piece of equipment for all but the shortest rides."
>
> – Every cyclist ever

Bidon aims to be a simple, easy to use, and flexible data handling library.

Data comes in many forms and the things we want to do with it are varied. Over the years I've developed a number of idioms for working with databases, spreadsheets and other data sources, and I've collected those in Bidon.

Bidon's main features are:

- A thin wrapper over DB API 2 that makes common database operations very simple, but that gets out of the way when you want to do something more complex. It gives you some of the nice things of an ORM without all the cruft. I call it a nORM.
- An API that lets you access .xls, .xlsx, .ods and .csv files in a consistent manner.
- A JSON patch implementation
- A collection of utility functions

This library has no strictly required dependencies, although some parts of it do require third-party
libraries.
