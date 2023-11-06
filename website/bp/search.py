import pickle
import time
from functools import cache

from autotraders.faction.contract import Contract
from autotraders.paginated_list import PaginatedList
from autotraders.ship import Ship
from flask import Blueprint, render_template, request

from website.paginated_return import paginated_return
from website.search import read_query, quick_weight, check_filters_waypoint, weight, check_filters_system, \
    check_filters_faction, check_filters_ship, check_filters_contract
from website.session import get_session
from website.wrappers import token_required

search_bp = Blueprint("search", __name__)


@cache
def load_system_data():
    return pickle.load(open("./data.pickle", "rb"))


@cache
def load_faction_data():
    return pickle.load(open("./factions.pickle", "rb"))


@search_bp.route("/search/")
def search():
    session = get_session()
    page = int(request.args.get("page", default=1))
    fast_search = bool(request.args.get("fast", default=False))
    t1 = time.time()
    raw_query = request.args.get("query")
    if raw_query is None:
        raw_query = ""
    query, filters = read_query(raw_query)
    to_query = ["system", "waypoint", "faction", "ship", "contract"]
    for is_filter in filters:
        if is_filter.name == "is":
            if is_filter.value == "ship":
                to_query = ["ship"]
            elif is_filter.value == "faction":
                to_query = ["faction"]
            elif is_filter.value == "map":
                to_query = ["system", "waypoint"]
            elif is_filter.value == "system":
                to_query = ["system"]
            elif is_filter.value == "waypoint":
                to_query = ["waypoint", "system"]
            elif is_filter.value == "contract":
                to_query = ["contract"]
    if "system" in to_query:
        system_data = load_system_data()
    else:
        system_data = []
    t1_2 = time.time()
    if "faction" in to_query:
        faction_data = load_faction_data()
    else:
        faction_data = []
    t1_3 = time.time()
    unweighted_map = []
    t1_4 = time.time()
    if "system" in to_query:
        for item in system_data:
            if quick_weight(query, str(item.symbol)) > -0.1:
                if check_filters_system(item, filters):
                    unweighted_map.append((item, weight(query, str(item.symbol))))
            if "waypoint" in to_query and (not fast_search or quick_weight(query, str(item.symbol)) > -0.1):
                for waypoint in item.waypoints:
                    if quick_weight(query, str(waypoint.symbol)) > 0 and check_filters_waypoint(
                            waypoint, filters
                    ):
                        unweighted_map.append(
                            (waypoint, weight(query, str(waypoint.symbol)))
                        )
    t1_5 = time.time()
    if "faction" in to_query:
        for item in faction_data:
            if (
                    quick_weight(query, item.symbol) > -0.25 or quick_weight(query, item.name) > -0.25
            ) and check_filters_faction(item, filters):
                unweighted_map.append((item, weight(query, str(item.symbol))))
    t1_6 = time.time()
    if "ship" in to_query and session is not None:
        ship_data = Ship.all(session)[1]
        for item in ship_data:
            if quick_weight(query, item.symbol) > -0.25 and check_filters_ship(item, filters):
                unweighted_map.append((item, weight(query, item.symbol)))
    if "contract" in to_query and session is not None:
        contract_data = Contract.all(session)[1]
        for item in contract_data:
            if quick_weight(query, item.contract_id) > -0.7 and check_filters_contract(
                item, filters
            ):
                unweighted_map.append((item, weight(query, str(item.contract_id))))
    amap = [
        item for item, c in sorted(unweighted_map, key=lambda x: x[1], reverse=True) if c > -0.5
    ]
    t2 = time.time()

    # print(t1_2 - t1, t1_3 - t1_2, t1_4 - t1_3, t1_5 - t1_4, t1_6 - t1_5, t2 - t1_6)

    def paginate(p, num_per_page):  # TODO: test properly
        return amap[(p - 1) * num_per_page: p * num_per_page], len(amap)

    paginated_list = PaginatedList(paginate, page, 100)
    new_li = paginated_return(paginated_list, page)

    return render_template(
        "search.html",
        query=raw_query,
        fast_search=fast_search,
        results=paginated_list,
        page=page,
        time=str(t2 - t1),
        li=new_li
    )
