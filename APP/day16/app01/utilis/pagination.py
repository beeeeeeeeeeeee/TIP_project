from django.utils.safestring import mark_safe


class Pagination(object):
    def __init__(self, request, queryset, page_param="page", page_size=10, plus=5):
        page = request.GET.get(page_param, "1")
        if page.isdecimal():
            page = int(page)
        else:
            page = 1
        self.page = page
        self.page_size = page_size
        self.start = (page - 1) * page_size
        self.end = page * page_size
        self.page_queryset = queryset[self.start: self.end]
        self.plus = plus

        total_count = queryset.count()
        total_page_count, div = divmod(total_count, page_size)
        if div:
            total_page_count += 1
        self.total_page_count = total_page_count

    def html(self):
        # 1 to total
        if self.total_page_count <= 2 * self.plus + 1:
            start_page = 1
            end_page = self.total_page_count
        else:
            # 1 to 10
            if self.page <= self.plus:
                start_page = 1
                end_page = 2 * self.plus + 1
            else:
                # last few page
                if (self.page + self.plus) > self.total_page_count:
                    start_page = self.total_page_count - 2 * self.plus
                    end_page = self.total_page_count
                # normal page
                else:
                    start_page = self.page - self.plus
                    end_page = self.page + self.plus

        page_str_list = []

        page_str_list.append("<li><a href='?page={}'>First Page</a></li>".format(1))

        if self.page > 1:
            prev = "<li><a href='?page={}'>«</a></li>".format(self.page - 1)
        else:
            prev = "<li><a href='?page={}'>«</a></li>".format(1)
        page_str_list.append(prev)

        for i in range(start_page, end_page + 1):
            if i == self.page:
                ele = "<li class='active'><a href='?page={}'>{}</a></li>".format(i, i)
            else:
                ele = "<li><a href='?page={}'>{}</a></li>".format(i, i)
            page_str_list.append(ele)

        if self.page < self.total_page_count:
            next_page = "<li><a href='?page={}'>»</a></li>".format(self.page + 1)
        else:
            next_page = "<li><a href='?page={}'>»</a></li>".format(self.total_page_count)
        page_str_list.append(next_page)

        page_str_list.append("<li><a href='?page={}'>Last Page</a></li>".format(self.total_page_count))

        search_string = """
            <li>
                <form style="float: left;margin-left: -1px" method="get">
                    <input name="page"
                           style="position: relative;float:left;display: inline-block;width: 80px;border-radius: 0;"
                           type="text" class="form-control" placeholder="Page">
                    <button style="border-radius: 0" class="btn btn-default" type="submit">Go</button>
                </form>
            </li>
            """

        page_str_list.append(search_string)
        page_string = mark_safe("".join(page_str_list))
        return page_string
