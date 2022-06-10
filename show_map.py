"""show_map.py
    defines limits of the bounding box and print map from user's selection.
"""
# Import libraries
import folium
import numpy as np
import webbrowser

def map_html(user_coord, degree):
    W = user_coord[1] - degree
    E = user_coord[1] + degree
    N = user_coord[0] + degree
    S = user_coord[0] - degree
    w = user_coord[1] - degree/2
    e = user_coord[1] + degree/2
    n = user_coord[0] + degree/2
    s = user_coord[0] - degree/2

    array_coord = np.array([user_coord[0], user_coord[1], N, W, N, E, S, E, S, W, user_coord[0], W, N, user_coord[1],
                            user_coord[0], E, S, user_coord[1],s ,w, n, w, n, e, s, e, user_coord[0], e, user_coord[0],
                            w, n, user_coord[1], s, user_coord[1],N,w,N,e,n,E,s,E,S,e,S,w,s,W,n,W])

    upper_left = (N, W)
    upper_right = (N, E)
    lower_right = (S, E)
    lower_left = (S, W)
    line_color = 'red'
    fill_color = 'red'
    weight = 2
    text = 'text'
    edges = [upper_left, upper_right, lower_right, lower_left]
    map_osm = folium.Map(location=user_coord, zoom_start=8)
    map_osm.add_child(folium.vector_layers.Polygon(locations=edges, color=line_color, fill_color=fill_color,
                                               weight=weight, popup=(folium.Popup(text))))
    for point in range(0, int(len(array_coord)/2)):
        requested_points_lat = str(array_coord[2 * point])
        requested_points_lon = str(array_coord[2 * point + 1])
        requested_point = [requested_points_lat, requested_points_lon]
        folium.CircleMarker(requested_point, radius=3).add_to(map_osm)

    #auto-open the map in browser
    map_osm.save('user_selection_map.html')
    html_page = f"{'user_selection_map.html'}"
    map_osm.save(html_page)
    # open in browser.
    new = 2
    webbrowser.open(html_page, new=new)


    print('\n Bounding box coordinates:\n----------------\nUpper left : {}\nUpper right : {}\nLower left : {}\nLower '
          'right : {} '
        .format(
        upper_left,
        upper_right,
        lower_left,
        lower_right))

    return array_coord