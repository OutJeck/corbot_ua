from country import Country

def example_fun():
    # to optimize the process, ie to use map creation
    # so that each tap does not have redundant attributes,
    # it was agreed to use our class on two fronts,
    # some functions will not allow you to use.
    # I will demonstrate by example, which will
    # show what opportunities our ADT has.


    # part for the normal use

    ua = Country("Ukraine")

    # represents country in iso3 format
    print('ISO3, Ukraine: ', ua.iso3)

    # prints the DataFrame
    # with information about deaths, confirmed cases and recovered in Ukraine.
    print('DataFrame:\n', ua.df)

    # prints the name of the country (Ukraine)
    print(ua)

    # prints the name of the country (Ukraine) in iso3 format
    print(ua.__repr__())

    # part for using map

    # in this case, our abstract data type receives
    # confirmed cases of coronavirus as an argument,
    # then the program will interpret it completely differently.

    confirmed = 15000  # the number of confirmed cases
    ua = Country("Ukraine", confirmed)

    # prints confirmed cases in Ukraine
    print('Confirmed cases:\n', ua.confirmed)

    # prints population in Ukraine
    print('Ukraine population:\n', ua.population)

    # displays information on the number of patients with coronavirus per one million
    print('Confirmed cases per one million:\n', ua.cpm)


if __name__ == '__main__':
    example_fun()
