from collections import deque
import random

class MaxHeap:
    def __init__(self):
        self.heap = []

    def push(self, item):
        self.heap.append(item)
        self._sift_up(len(self.heap) - 1)

    def pop(self):
        if len(self.heap) == 0:
            print("empty heap")
            return
        max_item = self.heap[0]
        last_item = self.heap.pop()
        if len(self.heap) > 0:
            self.heap[0] = last_item
            self._sift_down(0)
        return max_item

    def _sift_up(self, index):
        while index > 0:
            parent_index = (index - 1) // 2
            if self.heap[parent_index] < self.heap[index]:
                self.heap[parent_index], self.heap[index] = self.heap[index], self.heap[parent_index]
                index = parent_index
            else:
                break

    def _sift_down(self, index):
        while index * 2 + 1 < len(self.heap):
            left_child_index = index * 2 + 1
            right_child_index = index * 2 + 2 if index * 2 + 2 < len(self.heap) else left_child_index
            max_child_index = left_child_index if self.heap[left_child_index] > self.heap[right_child_index] else right_child_index
            if self.heap[index] < self.heap[max_child_index]:
                self.heap[index], self.heap[max_child_index] = self.heap[max_child_index], self.heap[index]
                index = max_child_index
            else:
                break

    def __len__(self):
        return len(self.heap)

class Graph:
    def __init__(self):
        self.usernodes = {}
        self.restaurantnodes = {}

    def add_user_node(self, key, data):
        if key not in self.usernodes:
            self.usernodes[key] = {"data": data, "neighbors": []}

    def add_restaurant_node(self, key, data):
        if key not in self.restaurantnodes:
            self.restaurantnodes[key] = {"data": data, "neighbors": []}

   
    def add_edge(self, from_node, to_node, node_type, rating):
        if node_type == "users":
            if from_node in self.usernodes and to_node in self.restaurantnodes:
                # Check if the edge already exists
                existing_edges = [edge[0] for edge in self.usernodes[from_node]["neighbors"]]
                if to_node not in existing_edges:
                    self.usernodes[from_node]["neighbors"].append((to_node, rating))# Include rating in the edge
                    
                existing_edges = [edge[0] for edge in self.restaurantnodes[to_node]["neighbors"]]
                if from_node not in existing_edges:
                    self.restaurantnodes[to_node]["neighbors"].append((from_node, rating))  # Include rating in the edge
                    
        elif node_type == "restaurants":
            if from_node in self.restaurantnodes and to_node in self.usernodes:
                # Check if the edge already exists
                existing_edges = [edge[0] for edge in self.restaurantnodes[from_node]["neighbors"]]
                if to_node not in existing_edges:
                    self.restaurantnodes[from_node]["neighbors"].append((to_node, rating))  # Include rating in the edge
                
                existing_edges = [edge[0] for edge in self.usernodes[to_node]["neighbors"]]
                if from_node not in existing_edges:
                    self.usernodes[to_node]["neighbors"].append((from_node, rating))  # Include rating in the edge
        else:
            print("Invalid node type. Please provide either 'users' or 'restaurants'.")

    def display_user_graph(self):
        print("User Nodes:")
        for node_key, node_data in self.usernodes.items():
            print("Node:", node_key)
            print("Data:", node_data["data"])
            print("Neighbors:")
            for neighbor_key in node_data["neighbors"]:
                neighbor_data = self.usernodes[neighbor_key]["data"]
                print("-", neighbor_data.name)
            print()

    def display_restaurant_graph(self):
        print("Restaurant Nodes:")
        for node_key, node_data in self.restaurantnodes.items():
            print("Node:", node_key)
            print("Data:", node_data["data"])
            print("Neighbors:")
            for neighbor_key in node_data["neighbors"]:
                neighbor_data = self.usernodes[neighbor_key]["data"]
                print("-", neighbor_data.name)
            print()

    
    def display_all_users(self):
        print("All Users:")
        for node_key, node_data in self.usernodes.items():
            print("Node:", node_key)
            print("Name:", node_data["data"].name)
            print("Favorite Cuisines:", ', '.join(node_data["data"].favorite_cuisines))
            print("Dietary Restrictions:", ', '.join(node_data["data"].dietary_restrictions))
            print("Budget Preferences:", ', '.join(node_data["data"].budget_preferences))
            print("Visited Restaurants:", ', '.join(node_data["data"].visited_restaurants))
            print()

    def display_all_restaurants(self):
        print("All Restaurants:")
        for node_key, node_data in self.restaurantnodes.items():
            average_rating = node_data["data"].get_average_rating()
            print("Node:", node_key)
            print("Name:", node_data["data"].name)
            print("Cuisine Type:", node_data["data"].cuisine_type)
            print("Dietary Restrictions:", node_data["data"].dietary_restrictions)
            print("Price Range:", node_data["data"].price_range)
            print("Rating:", average_rating)
            print("Zone:", node_data["data"].zone)
            print()

    def display_all_restaurants_names(self):
        print("All Restaurants:")
        for node_key, node_data in self.restaurantnodes.items():
            # print("Node:", node_key)
            print("Name:", node_data["data"].name)
            
    def add_node(self, key, data, node_type):
        if node_type == "users":
            self.add_user_node(key, data)
        elif node_type == "restaurants":
            self.add_restaurant_node(key, data)

    def display_graph(self, node_type):
        if node_type == "users":
            self.display_user_graph()
        elif node_type == "restaurants":
            self.display_restaurant_graph()

    def display_unique_menu_items(self):
        unique_items = set()
        for node_key, node_data in self.restaurantnodes.items():
            restaurant_profile = node_data["data"]
            unique_items.update(restaurant_profile.menu_items)

        print("Unique Menu Items:")
        for item in unique_items:
            print("-", item)

    def add_random_edges(self, n):
    # Hardcoded seed value for consistent randomization
        seed_value = 42
        random.seed(seed_value)

        users = list(self.usernodes.keys())
        restaurants = list(self.restaurantnodes.keys())

        # Select n random pairs of usernames and restaurant names
        random_usernames = random.sample(users, n)
        random_restaurants = random.sample(restaurants, n)
        
        # Hardcoded list of ratings for consistency
        hardcoded_ratings = [4.2, 3.5, 2.8, 4.0, 3.9, 4.5, 3.7, 4.1, 3.3, 3.8]

        for user, restaurant, rating in zip(random_usernames, random_restaurants, hardcoded_ratings):
            # Get the user profile instance
            user_profile = self.usernodes[user]["data"]
            # Call mark_visited_restaurant method of UserProfile
            user_profile.mark_visited_restaurant(user, restaurant, rating, self, self)
        
    def add_initial_restaurants(self):
        # Hardcoded initial restaurant data
        restaurant_data = [
            ("Pizza Palace", "Italian", "Vegetarian", "Moderate", 0,["Margherita Pizza", "Pepperoni Pizza", "Cheese Pizza"],"A"),
            ("Taco Time", "Mexican", "Vegan", "Expensive", 0,["Margherita Pizza", "Chicken Taco", "French Fries"],"B"),
            ("Sushi Garden", "Japanese", "Vegetarian", "Moderate", 0,["Veg Roll", "Sushi Platter", "French Fries"],"C"),
            ("Spice Avenue", "Indian", "Vegetarian", "Moderate", 0,["Margherita Pizza", "Mix Veg", "Veg Roll"],"D"),
            ("Burger Haven", "American", "Gluten-free", "Budget-friendly", 0,["Chicken Burger", "Pepperoni Pizza", "Pasta"],"E"),
            ("Pasta Paradise", "Italian", "Gluten-free", "Expensive", 0,["Cheese Pizza", "Red Sauce Pasta", "Pasta"],"F"),
            ("Tandoori Nights", "Indian", "Gluten-free", "Moderate", 0,["Mix Veg", "Butter Chicken", "Chicken Burger"],"I"),
            ("Salsa Fiesta", "Mexican", "Vegan", "Budget-friendly", 0,["Red Sauce Pasta", "Pepperoni Pizza", "Chicken Taco"],"J"),
            ("Sushi Express", "Japanese", "Vegetarian", "Budget-friendly", 0,["Veg Roll", "Sushi Platter", "Pasta"],"G"),
            ("Bella Italia", "Italian", "Vegan", "Budget-friendly", 0,["Red Sauce Pasta", "Pepperoni Pizza", "Pasta"],"H")
        ]

        # Add restaurants to the graph
        for name, cuisine, location, price_range, rating, menu_items,zone in restaurant_data:
            new_restaurant = RestaurantProfile(name, cuisine, location, price_range, rating, menu_items,zone)
            key = name.lower().replace(" ", "_")
            self.add_node(key, new_restaurant, "restaurants")

    def add_initial_users(self):
        # Hardcoded initial user data with additional preferences
        user_data = [
            ("Alice", ["Italian", "Japanese"], ["Vegetarian"], ["Budget-friendly"]),
            ("Bob", ["Mexican", "Indian"], ["Vegan"], ["Moderate"]),
            ("Charlie", ["Japanese"], ["Gluten-free"], ["Expensive"]),
            ("David", ["Italian", "Mexican"], ["Vegetarian", "Gluten-free"], ["Moderate"]),
            ("Eve", ["Indian"], ["Vegan"], ["Budget-friendly"]),
            ("Frank", ["Mexican", "Italian"], ["Vegetarian"], ["Moderate"]),
            ("Grace", ["Japanese", "Indian"], ["Gluten-free"], ["Expensive"]),
            ("Hannah", ["Mexican", "Italian"], [], ["Moderate"]),
            ("Ivy", ["Italian", "Indian"], ["Vegan", "Gluten-free"], ["Budget-friendly"]),
            ("Jack", ["Mexican", "Japanese"], [], ["Expensive"])
        ]

        # Add users to the graph
        for name, favorite_cuisines, dietary_restrictions, budget_preferences in user_data:
            new_user = UserProfile(name)
            for cuisine in favorite_cuisines:
                new_user.add_favorite_cuisine(cuisine)
            for restriction in dietary_restrictions:
                new_user.add_dietary_restriction(restriction)
            for budget in budget_preferences:
                new_user.add_budget_preference(budget)
            key = name.lower().replace(" ", "_")
            self.add_node(key, new_user, "users")

        # Add random edges between users and restaurants with random ratings
        for user_key in self.usernodes:
            user_node = self.usernodes[user_key]
            for restaurant_key in self.restaurantnodes:
                restaurant_node = self.restaurantnodes[restaurant_key]
                # Generate a random rating between 0 and 5
                rating = round(random.uniform(0, 5), 1)
                # Add edge with the random rating
                self.add_edge(user_key, restaurant_key, "users", rating)

    def get_top_restaurants(self):
        max_heap = MaxHeap()
        for node_key, node_data in self.restaurantnodes.items():
            restaurant_profile = node_data["data"]
            average_rating = restaurant_profile.get_average_rating()
            # Only add restaurants with non-zero average rating to the max heap
            if average_rating > 0:
                max_heap.push((average_rating, restaurant_profile.name))

        print("Top 5 Restaurants by Average Rating:")
        for _ in range(min(5, len(max_heap))):
            rating, name = max_heap.pop()
            print(f"{name}: {rating:.2f}")



class RestaurantProfile:
    def __init__(self, name, cuisine_type, dietary_restrictions, price_range, rating , menu_items,zone):
        self.name = name
        self.cuisine_type = cuisine_type
        self.dietary_restrictions = dietary_restrictions
        self.price_range = price_range
        self.rating = {}
        self.rate = rating
        self.menu_items = menu_items
        self.zone = zone

    def add_review(self, review):
        self.reviews.append(review)

    def display_profile(self):
        print("Restaurant Profile:")
        print(f"Name: {self.name}")
        print(f"Cuisine Type: {self.cuisine_type}")
        print(f"Zone: {self.zone}")
        print(f"Price Range: {self.price_range}")
        print(f"Rating: {self.rating}")

    def get_average_rating(self):
        total_ratings = sum(self.rating.values())
        num_ratings = len(self.rating)
        if num_ratings > 0:
            return total_ratings / num_ratings
        else:
            return 0

    def add_ratings(self , username , rating):
        self.rating[username] = rating 


class UserProfile:
    def __init__(self, name):
        self.name = name
        self.favorite_cuisines = []
        self.dietary_restrictions = []
        self.budget_preferences = []
        # self.location_preferences = []
        self.visited_restaurants = []
        # self.initialize_profile()

    def initialize_profile(self):
        print("Welcome to the User Profile Creator!")
        print("Let's gather some information about your preferences:")
        
        # Gather favorite cuisines
        while True:
            print("Select your favorite cuisines from the following options (comma-separated):")
            print("1. Italian")
            print("2. Mexican")
            print("3. Japanese")
            print("4. Indian")
            cuisines = input("Enter your choices (e.g., 1,2): ").split(",")
            invalid = False
            for cuisine in cuisines:
                if cuisine not in ['1', '2', '3', '4']:
                    print("Invalid input. Please enter valid choices.")
                    invalid = True
                    break
            if not invalid:
                break
        for cuisine in cuisines:
            if cuisine == '1':
                self.add_favorite_cuisine("Italian")
            elif cuisine == '2':
                self.add_favorite_cuisine("Mexican")
            elif cuisine == '3':
                self.add_favorite_cuisine("Japanese")
            elif cuisine == '4':
                self.add_favorite_cuisine("Indian")

        # Gather dietary restrictions
        while True:
            print("Select your dietary restrictions from the following options (comma-separated):")
            print("1. Vegetarian")
            print("2. Vegan")
            print("3. Gluten-free")
            restrictions = input("Enter your choices (e.g., 1,2): ").split(",")
            invalid = False
            for restriction in restrictions:
                if restriction not in ['1', '2', '3']:
                    print("Invalid input. Please enter valid choices.")
                    invalid = True
                    break
            if not invalid:
                break
        for restriction in restrictions:
            if restriction == '1':
                self.add_dietary_restriction("Vegetarian")
            elif restriction == '2':
                self.add_dietary_restriction("Vegan")
            elif restriction == '3':
                self.add_dietary_restriction("Gluten-free")

        # Gather budget preferences
        while True:
            print("Select your budget preferences from the following options (comma-separated):")
            print("1. Budget-friendly")
            print("2. Moderate")
            print("3. Expensive")
            budgets = input("Enter your choices (e.g., 1,2): ").split(",")
            invalid = False
            for budget in budgets:
                if budget not in ['1', '2', '3']:
                    print("Invalid input. Please enter valid choices.")
                    invalid = True
                    break
            if not invalid:
                break
        for budget in budgets:
            if budget == '1':
                self.add_budget_preference("Budget-friendly")
            elif budget == '2':
                self.add_budget_preference("Moderate")
            elif budget == '3':
                self.add_budget_preference("Expensive")

    def add_favorite_cuisine(self, cuisine):
        self.favorite_cuisines.append(cuisine)

    def add_dietary_restriction(self, restriction):
        self.dietary_restrictions.append(restriction)

    def add_budget_preference(self, budget):
        self.budget_preferences.append(budget)

    def mark_visited_restaurant(self, user_name, restaurant_name, rating, user_graph, restaurant_graph):
        user_node = user_name.lower().replace(" ", "_")
        restaurant_node = restaurant_name.lower().replace(" ", "_")

        if user_node in user_graph.usernodes and restaurant_node in restaurant_graph.restaurantnodes:
            restaurant_profile = restaurant_graph.restaurantnodes[restaurant_node]["data"]  # Retrieve RestaurantProfile object
            restaurant_profile.add_ratings(user_name, rating)  # Add rating to restaurant profile
            # Check if the user already visited the restaurant
            if restaurant_node not in user_graph.usernodes[user_node]["neighbors"]:
                # Add edge between user and restaurant
                user_graph.add_edge(user_node, restaurant_node, "users", rating)
                user_graph.add_edge(restaurant_node, user_node, "restaurants", rating)

                # Update visited restaurants list
                user_profile = user_graph.usernodes[user_node]["data"]
                user_profile.visited_restaurants.append(restaurant_name)

                # Display information
##                print(f"{user_name} visited {restaurant_name} and rated it {rating}.")

##                # Display updated neighbor lists
##                print("User Neighbors after adding edge:", user_graph.usernodes[user_node]["neighbors"])
##                print("Restaurant Neighbors after adding edge:", restaurant_graph.restaurantnodes[restaurant_node]["neighbors"])
##
##                # Display user and restaurant profiles
##                print("\nUser Profile:")
##                user_profile.display_profile()
##
##                print("\nRestaurant Profile:")
##                restaurant_profile = restaurant_graph.restaurantnodes[restaurant_node]["data"]
##                restaurant_profile.display_profile()
            else:
                print(f"{user_name} has already visited {restaurant_name}.")
        else:
            print(f"User '{user_name}' or restaurant '{restaurant_name}' not found.")


    def display_profile(self):
        print("User Profile:")
        print(f"Name: {self.name}")
        print(f"Favorite Cuisines: {', '.join(self.favorite_cuisines)}")
        print(f"Dietary Restrictions: {', '.join(self.dietary_restrictions)}")
        print(f"Budget Preferences: {', '.join(self.budget_preferences)}")
        print(f"Visited Restaurants: {', '.join(self.visited_restaurants)}")


def add_restaurant(graph):
    print("Adding a new restaurant:")
    name = input("Enter restaurant name: ")
    
    # Gather cuisine type
    print("Select cuisine type:")
    print("1. Italian")
    print("2. Mexican")
    print("3. Japanese")
    print("4. Indian")
    cuisine_choice = input("Enter your choice (1-4): ")
    cuisines = ["Italian", "Mexican", "Japanese", "Indian"]
    cuisine_type = cuisines[int(cuisine_choice) - 1]

    # select dietary restrictions
    print("Select the dietary restrictions you follow:")
    print("1. Vegetarian")
    print("2. Vegan")
    print("3. Gluten-free")
    dietary_restrictions_choice = input("Enter your choice (1-3): ")
    dietary_restrictions = ["Vegetarian", "Vegan", "Gluten-free"]
    dietary_restrictions = dietary_restrictions[int(dietary_restrictions_choice) - 1]

    # Gather price range
    print("Select your restaurant's price range:")
    print("1. Budget-friendly")
    print("2. Moderate")
    print("3. Expensive")
    price_choice = input("Enter your choice (1-3): ")
    price_ranges = ["Budget-friendly", "Moderate", "Expensive"]
    price_range = price_ranges[int(price_choice) - 1]

    #select the zone
    print("Enter restaurants zone:")
    zone = input("Select among (A-J) : ")

    # Gather menu items
    menu_items = input("Enter menu items (comma-separated): ").split(",")

    new_restaurant = RestaurantProfile(name, cuisine_type, dietary_restrictions, price_range, 0, menu_items,zone)
    key = name.lower().replace(" ", "_")
    graph.add_node(key, new_restaurant, "restaurants")
    print("Restaurant added successfully!")




def add_user(graph):
    name = input("Enter your name: ")
    new_user = UserProfile(name)
    new_user.initialize_profile()  # Call initialize_profile method here
    key = name.lower().replace(" ", "_")
    graph.add_node(key, new_user, "users")
    print("User added successfully!")


def login_user(graph):
    name = input("Enter your name: ").lower().replace(" ", "_")
    if name in graph.usernodes:
        user_profile = graph.usernodes[name]["data"]
        user_profile.display_profile()
    else:
        print("User not found!")
    return name #check


def recommend_restaurant(graph, user_name):
    recommended_restaurants = []
    recommended_restaurants_profile = []
    user_node = user_name.lower().replace(" ", "_")
    
    if user_node in graph.usernodes:
        user_profile = graph.usernodes[user_node]["data"]
        user_preferences = {
            "favorite_cuisines": user_profile.favorite_cuisines,
            "dietary_restrictions": user_profile.dietary_restrictions,
            "budget_preferences": user_profile.budget_preferences
        }
        
        visited_restaurants = set(user_profile.visited_restaurants)
        
        # BFS traversal starting from the user node
        queue = deque([(user_node, 0)])  # Initialize queue with user node and depth 0
        visited = set()  # Set to keep track of visited nodes
        
        while queue:
            current_node, depth = queue.popleft()  # Dequeue the current node and its depth
            
            if depth > 1:
                break  # Limiting the traversal depth
            
            if current_node in visited:
                continue  # Skip if the current node has been visited
            
            visited.add(current_node)  # Mark the current node as visited
            
            # If the current node is a restaurant node and has been visited by the user
            if current_node in graph.restaurantnodes and (current_node in visited_restaurants or graph.restaurantnodes[current_node]["data"].name in visited_restaurants):
                restaurant_data = graph.restaurantnodes[current_node]
                restaurant_profile = restaurant_data["data"]
                
                # Check if the restaurant matches the user's preferences
                if any(pref in restaurant_profile.cuisine_type for pref in user_preferences["favorite_cuisines"]) \
                    or any(pref in restaurant_profile.location for pref in user_preferences["dietary_restrictions"]) \
                    or any(pref in restaurant_profile.price_range for pref in user_preferences["budget_preferences"]):
                    # Use the average rating directly from the RestaurantProfile
                    average_rating = restaurant_profile.get_average_rating()
                    if average_rating > 0:
                        recommended_restaurants.append((restaurant_profile.name, average_rating))
                        recommended_restaurants_profile.append(restaurant_profile)
            
            # Enqueue neighbors of the current node
            if current_node in graph.usernodes:
                for neighbor_key, _ in graph.usernodes[current_node]["neighbors"]:
                    queue.append((neighbor_key, depth + 1))  # Enqueue neighbor with increased depth
        
        # Sort recommended restaurants by rating in descending order
        recommended_restaurants.sort(key=lambda x: x[1], reverse=True)

        # Use a stack to maintain top 2 restaurants
        top_restaurants = []
        for restaurant_name, rating in recommended_restaurants:
            if len(top_restaurants) < 5:
                top_restaurants.append((restaurant_name, rating))
            elif rating > top_restaurants[1][1]:
                if rating > top_restaurants[0][1]:
                    top_restaurants.pop()
                    top_restaurants.append((restaurant_name, rating))
                else:
                    top_restaurants.pop(0)
                    top_restaurants.insert(0, (restaurant_name, rating))

        #recommedation as per location :
        class node:
            def __init__(self,distance_from_user,restaurant_name) :
                self.distance_from_user = distance_from_user
                self.restaurant_name = restaurant_name
                
        fl = input("Do you want recommendation as per location (Yes,No)? ")
        fl = fl.lower()
        if(fl == "no") :
            print("Top 5 Recommended Restaurants:")
            for i, (restaurant_name, rating) in enumerate(top_restaurants, 1):
                print(f"{i}. {restaurant_name} (Rating: {rating})")
##            for i,item in enumerate(recommended_restaurants_profile) :
##                print(f"{str(i+1)}. {item.name}")
        elif(fl == "yes") :
            zone_list = ["A","B","C","D","E","F","G","H","I","J"]
            flag = 1
            distance_list=[]
            #taking zone input
            while(flag == 1):
                zone = input("Enter your zone among (A-J) : ")
                zone = zone.upper()
                if(zone not in zone_list) :
                    print("Incorrect input , Re-enter zone")
                    continue
                else :
                    #finding the distance between the user and all the filtered location
                    nodelist = []
                    for item in recommended_restaurants_profile :
                        user_zone_ascii = ord(zone) #storing the ascii value of the user zone alphabet
                        restaurant_zone = item.zone # storing the zone alphabet of the restaurant
                        restaurant_zone_ascii = ord(restaurant_zone) #storign the ascii value of the restaurant zone alphabet
                        distance = user_zone_ascii - restaurant_zone_ascii #calculating the distance by difference
                        distance = abs(distance) #in case of negative values converting it into absolute value

                        distance_node = node(distance,item.name) #creating an object with distance and the restuarant
                        nodelist.append(distance_node) #storing the nodes into the list

                    #printing the first two recommended restaurants
                    sorted_nodelist = sorted(nodelist, key=lambda x: x.distance_from_user)
                    for node in sorted_nodelist[:2]:
                        print(node.restaurant_name)
                    flag = 0
    else:
        print(f"User '{user_name}' not found.")

def recommend_restaurant_nonvisit(graph, user_name):
    recommended_restaurants = []
    recommended_restaurants_profile = []
    user_node = user_name.lower().replace(" ", "_")
    
    if user_node in graph.usernodes:
        user_profile = graph.usernodes[user_node]["data"]
        user_preferences = {
            "favorite_cuisines": user_profile.favorite_cuisines,
            "dietary_restrictions": user_profile.dietary_restrictions,
            "budget_preferences": user_profile.budget_preferences
        }
        
        visited_restaurants = set(user_profile.visited_restaurants)
        
        # Iterate through all restaurant nodes in the graph
        for restaurant_node, restaurant_data in graph.restaurantnodes.items():
            restaurant_name = restaurant_data["data"].name

            # Check if the restaurant has not been visited by the user
            if restaurant_node not in visited_restaurants and restaurant_name not in visited_restaurants:
                restaurant_profile = restaurant_data["data"]

                # Check if the restaurant matches the user's preferences
                if any(pref in restaurant_profile.cuisine_type for pref in user_preferences["favorite_cuisines"]) \
                    or any(pref in restaurant_profile.dietary_restrictions for pref in user_preferences["dietary_restrictions"]) \
                    or any(pref in restaurant_profile.price_range for pref in user_preferences["budget_preferences"]):
                    # Use the average rating directly from the RestaurantProfile
                    average_rating = restaurant_profile.get_average_rating()
                    if average_rating > 0:
                        recommended_restaurants.append((restaurant_name, average_rating))
                        recommended_restaurants_profile.append(restaurant_profile)

        # Sort recommended restaurants by rating in descending order
        recommended_restaurants.sort(key=lambda x: x[1], reverse=True)

        # Use a stack to maintain top 2 restaurants
        top_restaurants = []
        for restaurant_name, rating in recommended_restaurants:
            if len(top_restaurants) < 5:
                top_restaurants.append((restaurant_name, rating))
            elif rating > top_restaurants[1][1]:
                if rating > top_restaurants[0][1]:
                    top_restaurants.pop()
                    top_restaurants.append((restaurant_name, rating))
                else:
                    top_restaurants.pop(0)
                    top_restaurants.insert(0, (restaurant_name, rating))

        #recommedation as per location :
        class node:
            def __init__(self,distance_from_user,restaurant_name) :
                self.distance_from_user = distance_from_user
                self.restaurant_name = restaurant_name
                
        fl = input("Do you want recommendation as per location (Yes,No)? ")
        fl = fl.lower()
        if(fl == "no") :
            print("Top 5 Recommended Restaurants:")
            for i, (restaurant_name, rating) in enumerate(top_restaurants, 1):
                print(f"{i}. {restaurant_name} (Rating: {rating})")
##            for i,item in enumerate(recommended_restaurants_profile) :
##                print(f"{str(i+1)}. {item.name}")
        elif(fl == "yes") :
            zone_list = ["A","B","C","D","E","F","G","H","I","J"]
            flag = 1
            distance_list=[]
            #taking zone input
            while(flag == 1):
                zone = input("Enter your zone among (A-J) : ")
                zone = zone.upper()
                if(zone not in zone_list) :
                    print("Incorrect input , Re-enter zone")
                    continue
                else :
                    #finding the distance between the user and all the filtered location
                    nodelist = []
                    for item in recommended_restaurants_profile :
                        user_zone_ascii = ord(zone) #storing the ascii value of the user zone alphabet
                        restaurant_zone = item.zone # storing the zone alphabet of the restaurant
                        restaurant_zone_ascii = ord(restaurant_zone) #storign the ascii value of the restaurant zone alphabet
                        distance = user_zone_ascii - restaurant_zone_ascii #calculating the distance by difference
                        distance = abs(distance) #in case of negative values converting it into absolute value

                        distance_node = node(distance,item.name) #creating an object with distance and the restuarant
                        nodelist.append(distance_node) #storing the nodes into the list

                    #printing the first two recommended restaurants
                    sorted_nodelist = sorted(nodelist, key=lambda x: x.distance_from_user)
                    for node in sorted_nodelist[:2]:
                        print(node.restaurant_name)
                    flag = 0

            

        
        
    else:
        print(f"User '{user_name}' not found.")


def recommend_restaurant_by_food(graph):
    food_item = input("Enter a food item: ")

    matching_restaurants = []
    for node_key, node_data in graph.restaurantnodes.items():
        restaurant_profile = node_data["data"]
        if food_item in restaurant_profile.menu_items:
            average_rating = restaurant_profile.get_average_rating()
            matching_restaurants.append((restaurant_profile.name, average_rating))

    # Sort matching restaurants by rating in descending order
    matching_restaurants.sort(key=lambda x: x[1], reverse=True)

    print(f"Restaurants offering '{food_item}':")
    for i, (restaurant_name, rating) in enumerate(matching_restaurants[:], 1):
        print(f"{i}. {restaurant_name} (Average Rating: {rating})")




def main():
    graph = Graph()
    graph.add_initial_restaurants()
    graph.add_initial_users()
    graph.add_random_edges(10)

    c = "yes"
    while c != "no":
        print("WELCOME TO TASTE SPOTTER")
        print("Enter your choice - ")
        print("1) Add a restaurant")
        print("2) Add a user")
        print("3) Login")
        print("4) Top 5 restaurants")
        print("5) Display all restaurants")
        print("6) Display all users")
        print("7) Exit")
        ch = int(input())

        if ch == 1:
            add_restaurant(graph)

        elif ch == 2:
            add_user(graph)

        elif ch == 3:
            name = login_user(graph)
            c1 = "yes"
            while c1!="no":
                print("Enter an option")
                print("1) Recommend restaurants")
                print("2) Give review to a restaurant")
                print("3) Logout")
                choice = int(input())
                if choice == 1:
                    print("Enter an option")
                    print("1) Recommendation from visited restaurants")
                    print("2) Recommendation from non visited restaurants")
                    print("3) Recommend a restaurant based on a food item")
                    c2 = int(input())
                    if c2 == 1:
                        recommend_restaurant(graph, name)
                    elif c2 == 2:
                        recommend_restaurant_nonvisit(graph, name)
                    elif c2 == 3:
                        graph.display_unique_menu_items()
                        recommend_restaurant_by_food(graph)
                elif choice == 2:
                    graph.display_all_restaurants_names()
                    user_name = name
                    restaurant_name = input("Enter restaurant name: ")
                    rating = float(input("Enter your rating (0-5): "))  # Prompt for rating input
                    if user_name in graph.usernodes:
                        user_profile = graph.usernodes[user_name]["data"]
                        user_profile.mark_visited_restaurant(user_name , restaurant_name, rating, graph, graph)  # Pass graph twice
                    else:
                        print("User not found!")
                elif choice == 3:
                    break
                print("Do you want to continue : (yes/no)")
                c1 = input()


        elif ch == 4:
            graph.get_top_restaurants()
        
        elif ch == 5:
            graph.display_all_restaurants()

        elif ch == 6:
            graph.display_all_users()

        elif ch == 7:
            print("Thank you")
            c=="no"
            break

        print("Do you want to continue - (yes/no)")
        c = input()
        if c=="no":
            print("Thank you")
            exit


if __name__ == "__main__":
    main()
