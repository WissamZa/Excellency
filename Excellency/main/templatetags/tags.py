from django import template
from account.models import User
register = template.Library()


@register.filter(name="getlist")
def getlist(request_dictionary, key):
    return request_dictionary.getlist(key)


@register.filter(name="rate_average")
def rate_average(user: User):
    orders = user.lawyer.all()
    order_count = orders.count()
    if order_count == 0:
        return 0
    sum_rating = 0
    for order in orders:
        sum_rating += order.rating.rate
    aver = sum_rating / order_count
    return aver


@register.filter(name='range')
def _range(_min, max):
    return range(1, max + 1)
    # @register.filter(name='range')
    # def _range(_min, args=None):
    #    _max, _step = None, None
    #    if args:
    #       if not isinstance(args, int):
    #          _max, _step = map(int, args.split(','))
    #       else:
    #          _max = args + 1
    #    args = filter(None, (_min, _max, _step))
    #    return range(*args)


# @register.filter(name='base_category')
# def base_category(a):
#    return Product.categories_choices.choices


@register.filter(name='image_name')
def image_name(name: str):
    return name.split("/")[-1]

    # @register.filter(name="random")
    # def random_int(a):
    #    return random.choice(plant_count())[0]

    # @register.simple_tag
    # def number_of_plants(request):
    #    return plant_count() - 1
