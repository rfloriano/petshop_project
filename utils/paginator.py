from django.core.paginator import Paginator, InvalidPage, Page

__all__ = ('BetterQuerySetPaginator', 'InvalidPage')

class BetterPaginator(Paginator):
    """
    An enhanced version of the QuerySetPaginator.

    >>> my_objects = BetterQuerySetPaginator(queryset, 25)
    >>> page = 1
    >>> context = {
    >>>     'my_objects': my_objects.get_context(page),
    >>> }
    """
    number = 1
    def page(self, number):
        "Returns a Page object for the given 1-based page number."
        self.number = self.validate_number(number)
        bottom = (self.number - 1) * self.per_page
        top = bottom + self.per_page
        if top + self.orphans >= self.count:
            top = self.count
        return Page(self.object_list[bottom:top], self.number, self)

    def _get_page_range(self, range_gap=5):
        """
        Returns a 1-based range of pages for iterating through within
        a template for loop.
        """
        if self.number > 5:
            start = self.number-range_gap
        else:
            start = 1

        if self.number < self.num_pages-range_gap:
            end = self.number+range_gap+1
        else:
            end = self.num_pages+1
        return range(start, end)
    page_range = property(_get_page_range)

