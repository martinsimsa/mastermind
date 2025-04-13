# Technická dokumentace
Tohle je technická dokumentace programu Mastermind - testování algoritmů

## Obsah
Dokumentace obsahuje popisy jednotlivých funkcí a jejich propojení. 
- [Process](#installation)
- [Classes](#classdescriptions)
- [Functions](#functions)
- [main_function](#main_function)
- [Global variables]

## Classes
### struct cmp_str
 - struct with comparison function used for comparing keys in maps that use const char* as a key.

### struct Comparator
 - struct for comparing Node objects in the queue in A* algorithm

### class Node
Objects of this class are nodes in the 2D grid which corresponds to our map. 
#### Attributes:
 - g - the "distance" of the node from the start in A* algorithm
 - h - heuristic "distance" from the node to finish
 - f - g + h - used to choose nodes closer to finish
 - coordinates - pointer to two coordinates (x and y) of each node, position in the 2D grid from
 - open - boolean shows if we have processed the node in the A* algorithm. (true - we haven't, false - we have)
 - parent_node - pointer to the previous node in the A* algorithm, used for backtracking the route
 - cost - cost of running through this node (according to where below which object on the map the node is placed)
 - object_class - category of the object the node is located below - used when avoiding certain categories

#### Methods:
 - Node() - constructor, set open to true and cost to, minimal cost of running through a node
 - set_coordinates(int i, int j) - sets coordinates

### class Object
Objects of this class are used for all objects drawn on the map.
#### Attributes:
 - id - number assigned to the symbol this object represent (pavement, building etc.). Different in each .omap file.
 - type - type of the object. 2 - line, 4, 16 - polygon, rest we aren't concerned about
 - buffer - the size of the buffer I want to apply to the object. Half of the width of the line symbol.
 - count - the count of coordinates of the object
 - coords - array of the pairs of coordinates (x,y). Size count x 2
 - cost - cost of running through this object, minimum is 10, larger with lower running speed.
 - additive cost - extra cost of running if the object is used as second layer (ex. hatched areas).
 - extremy - array of four coordinates that show the extreme x and y values (minimum and maximum), ordered x min, x max, y min, y max.
 - object_class - category of the object the node is located below - used when avoiding certain categories
#### Methods:
 - Object() - constructor, cost is zero in default - there are some objects which do not contribute to the running speed


## Functions

inline bool file_exists (const std::string& name)
 - checks if a file exists according to the name, returns bool

int char_to_int(char* number)
 - takes char* (ex. '18665') and returns integer number (18665)

void set_path_and_options(std::string* path, bool* initilize_grid_costs, bool* run_through_midpoint)
 - function that behaves with the user
 - takes file path to the .omap file (without the .omap to help with saving other files later), checks if entered file path is valid
 - takes response if we want to upgrade the saved grid which we use for the A* algorithm
 - takes response if we want to run through a midpoint on the map
 - returns these values through pointers

void set_uncrossable_classes(int* dont_run_through_class)
 - prints the list of possible categories to choose from for avoiding certain objects
 - gets the response of which categories of objects we want to avoid

void <span style="color:yellow">build maps </span>(std::map<const char*, int, cmp_str>& code_to_cost, std::map<const char*, int, cmp_str>& code_to_additive_cost, std::map<const char*, int, cmp_str>& code_to_buffer, std::map<const char*, int, cmp_str>& code_to_object_class)
 - builds maps for assigning characteristics to objects, manually written
 - code_to_cost - cost of running through objects
 - code_to_additive_cost - additional cost of running
 - code_to_buffer - size with which we want to enlargen line symbols by - to occupy space for finding points in the grid below these objects

void <span style="color:yellow"> create_symbol_dictionary</span> (XMLElement* rootelement,
	std::map<const char*, int, cmp_str>& code_to_cost,
	std::map<const char*, int, cmp_str>& code_to_additive_cost,
	std::map<const char*, int, cmp_str>& code_to_buffer,
	std::map<int, char*>& id_to_code,
	std::map<int, int>& id_to_type,
	int* start_and_finish_id,
	int* line_id,
	int* control_point_id,
	int* bridge_id)
 - Browses through the symbol set in the .omap file
 - creates id_to_type map from symbol id to its type (line/polygon)
 - creates id_to_code map from symbol id to the official code from ISSPROM.
 - finds ids of start, finish, course line, control poin and bridge - used later

Node*** <span style="color:yellow">set_grid </span>(int* extremy, int interval, int* grid_dimensions)
 - Creates grid of Node objects. It represents our map
 - The distance between neighbouring nodes in 4-neighborhood I set to 282 units because the width of uncrossable lines is at least 400 units. That means that if there is an uncrossable line and if we go from point to point in the 8-neighborhoood, we won't be able to jump over it.
 - The grid spans over the area of all objects - from variable extremy, added a bit extra for its range at the end (+8)

void <span style="color:yellow">add_list_of_coordinates_and_find_extremes </span>(const char* coords_text, int*& extremy, Object* object, int count)
 - Takes text with coordinates of one object as parameters
 - splits the coordinates, updates global extreme values (extremy) - passing as reference
 - adds the coordinates to the object

void <span style="color:yellow">process_objects_from_xml </span>(int*& extremy, XMLNode* objects, Object** list_of_objects,
	std::map<int, char*> id_to_code,
	std::map<int, int> id_to_type,
	std::map<const char*, int, cmp_str> code_to_cost,
	std::map<const char*, int, cmp_str> code_to_additive_cost,
	std::map<const char*, int, cmp_str> code_to_buffer,
	int* start_and_finish_id,
	int* start_and_finish_index,
	std::map<const char*, int, cmp_str> code_to_object_class,
	int* control_point_id,
	int* control_point_index)
 - Browses through the list of objects and adds attributes to the Object objects
 - returns start and finish indexes, control point index through pointers
 - if the object is in code_to_cost map (affects running cost), we need to process it
 - adds object class to current object according to the object code
 - runs the add_list_of_coordinates_and_find_extremes function
 - adds count, buffer, type, cost, additive_cost to the object attributes
 - updates local extremes with buffer

bool <span style="color:yellow">check_indexes </span>(int* start_and_finish_index, int* control_point_index, bool* run_through_midpoint)
 - Checks if there are start, finish and midpoint objects in the map file.
 - Checking if we need to terminate program before it would crash

void <span style="color:yellow">transfer_object_costs_to_grid </span>(Node*** grid, Object* object, multipolygon geometry_object) {
 - Takes points inside local extreme values of the object
 - For all of them checks if the point is inside the object
 - If so, adds the cost of the object to the grid of class Node nodes
 - adds additive cost too.

void <span style="color:yellow">add_buffer_to_object </span>(Node*** grid, Object* object, int* extremy, int* bridge_id)
 - Takes object, switches its coordinates to the scale of our grid
 - According to the type, and buffer, it adds buffer using boost::geometry::strategy::buffer (see citation part)
 - Before the algorithm, I transform the objects into boost::geometry::model linestring for line or polygon for polygon
 - join_strategy - join_miter for straight (sharp) joins
 - end_strategy - end_flat for flat ending where the line originally ended
 - point_strategy - point_square - I dont really use it, but points of uncrossable objects would be square
 - side_strategy - side_straight - to keep the edge straight
 - for bridge, it makes the shape of bridge - two uncrossable lines next to each other which we can run inbetween
 - calls the function transfer_object_costs_to_grid with the boost geometry multipolygon - native result from buffer

void <span style="color:yellow">browse_objects_for_transfering_costs </span>(Node*** grid, Object** list_of_objects, int count, int* extremy, std::map<int, char*> id_to_code, std::map<const char*, int, cmp_str> code_to_cost, int* bridge_id) {
 - goes through objects and calls function add_buffer_to_object if the object affects the runnability

void <span style="color:yellow">convert_index_to_coordinates </span>(int* extremy, int* start_and_finish_index, Object** objects, int* control_point_index, int* start_and_finish_coordinates, int* control_point_coordinates) {
 - takes the indexes of start and finish and returns their coordinates in the grid dimensions

void <span style="color:yellow">check_points_positions </span>(Node*** grid, int* start_and_finish_coordinates, int* control_point_coordinates, bool* terminate_program) {
 - Checks if the start, finish and midpoint lie in uncrossable area - it would mean, I can't reach it
 - Used for terminating program with error message

double <span style="color:yellow">heuristic </span>(Node* current_node, Node* finish_node)
 - returns the euclidean distance of two nodes in the grid 

void <span style="color:yellow">find_fastest_path </span>(Node*** grid, int* start_and_finish_coordinates, int* grid_dimensions, int* dont_run_through_class) {
 - The A* algorithm
 - creates priority_queue with Node* objects as stored elements, they are compared using the Comparator function (compares the f distance)
 - pushes start Node to the queue
 - runs A* algorithm:
	- while the queue is nonempty, takes the top node, the node with the lowest number f - sum of the traveled distance from start and heuristic distance towards the finish
	- if the node has already been visited, we continue
	- we close the node - we can't get to it any shorter way
	- if we reach finish, we end here
	- otherwise we check all nodes from its 8-neighbourhood
	- If they are inside the grid, they aren't uncrossable (cost != -1) and we haven't processed then (node->open), we proceed
	- if the node is in forbidden category/class of objects, we continue
	- otherwise we count the distances g, h, f.
	- if we havent reached this node or we have reached this node with higher cost, we put it in the queue with new distances
	- we dont forget to set the parent node to the node we are currently processing

void <span style="color:yellow">clear_grid_after_a_star </span>(Node*** grid, int* grid_dimensions)
 - clears grid of data from A* algorithm. Used in case of route across midpoint.

void <span style="color:yellow">backtrack_and_add_route </span>(Node*** grid, int* start_and_finish_coordinates, XMLElement* rootelement, int* line_id, int* extremy, XMLDocument* doc_pointer) {
 - backtrackts the shortest route and adds a new object element into the xml file - draws a line
 - if finish doesnt have a parent, it can't be reached and we can't wrote a line
 
void <span style="color:yellow">export_grid </span>(Node*** grid, std::string path, int* grid_dimensions)
 - save the grid to a file to save time in more repetitions

void <span style="color:yellow">import_grid </span>(Node***& grid, std::string path, int* grid_dimensions) {
 - imports grid data (costs, object class) and writes it into grid


 ## main_function
 int <span style="color:yellow">main </span>()

 #### getting input
 Firstly, we get input from the user using set_path_and_options and set_uncrossable_classes functions.

 #### .omap file processing
 Secondly, we load the .omap file using tinyxml2. We load it into XMLDocument, find the objects node, get the count of all objects in the map. We also initialize list of all object in the file which we will be using later.

 #### dictionaries
 Next, we build the maps connecting the codes of symbols with their characterictics, runnability (build_maps). We also browse through all symbols in the file, get important ids of symbols and connect symbol IDs to symbol code - id_to_code map. (create_symbol_dictionary).

 #### object processing
 Then, we browse through the objects in xml and we assign them their attributes. (process_objects_from_xml).
 Afterwards, we check if there is start, finish, potentionally midpoint in the map. (check_indexes)
 If they are missing, we terminate the program. We also find the coordinates of start, finish and the midpoint using the index of particular objects in the list of objects (convert_index_to_coordinates)

 #### setting up grid
 We initilize grid of Node nodes that we will use for the A* algorithm. (set_grid) If we need to update the grid, we browse through all objects and transfer their costs into the grid. (browse_objects_for_transfering_costs -> add_buffer_to_object -> transfer_object_costs_to_grid)
 Then we export the grid to use for next times. If we don't need to upgrade the grid from last actualization, we just import grid costs and object classes from saved file (import_grid).
 We also check the position of the start, finish and midpoint and terminate the program if they lie on an uncrossable node. (check_points_position)

 #### A* algorithm
 If we are running through midpoint, we run the A* algorithm (find_fastest_path) firstly to the midpoint, then we clear the grid (clear_grid_after_a_star) and run the A* algorithm again from the midpoint to the finish. After backtracking the route (backtrack_and_add_route), we get eventually two lines touching in the midpoint.
 Otherwise, we just run the A* algorithm from start to finish. 

 #### Export and end
 In the end, we just save the xml tree with the new route into a new .omap file with _route.omap ending. 
 Now we can show the result.



## global variables
 - std::string* path - path to the .omap file without .omap.
 - bool* initilize_grid_costs - true if user wants to upgrade costs in the map grid, if they made changes to the objects in the map
 - bool* run_through_midpoint - boolean to check if user wants to run through a midpoint on the map (true - run through midpoint, false - don't)
 - int* dont_run_through_class - array of ints to check, which classes/categories of objects we want to avoid. 0 - nothing happens, 1 - we avoid this class, class 1 corresponds to the index 0 etc.
 - XMLDocument doc - variable to store the .omap file
 - XMLElement* rootelement - pointer to the root element of doc
 - XMLDocument* doc_pointer - pointer to doc, passed as an argument to some functions to change doc inside of the functions
 - XMLNode* current_node
 - XMLNode* objects - pointer to the node objects in the .omap file structure, it stores the list of objects inside
 - int count_of_objects - stores the amount of objects in the .omap file, used to initilize the list of object and for browsing through them
 - Object** list_of_objects - array of Object* objects used to store all the objects on the map with its attributes (cost of running, buffer etc.)
 - std::map <const char*, int, cmp_str> code_to_cost - map with codes from ISSprOM 2019 as keys and cost of running through the objects as values. It uses str_cmp function as a function to compare const char the pointers point to.
 - std::map <const char*, int, cmp_str> code_to_additive_cost - map with codes from ISSprOM 2019 as keys and additive cost of running through the object of this symbol as values. The object is a hatching or another additional layer to the symbol underneath.
 - std::map <const char*, int, cmp_str> code_to_buffer - map with codes from ISSprOM 2019 as keys and the additional width of the symbol (line object in .omap file appears as a rectangular with width) as values. 
 - std::map <const char*, int, cmp_str> code_to_object_class - map with codes from ISSprOM 2019 as keys and the class of the symbol as values. Classes are used when choosing those user wants to avoid.
 - std::map <int, int> id_to_type - map with symbol IDx from the .omap file as keys and the symbol's type (line = 2/polygon = 4/16) as a value.
 - std::map <int, char*> id_to_code - map with symbol IDs from the .omap file as a key and the ISSprOM 2019 codes of the symbols as values. Used when we want to link IDs with the symbol's attributes (cost, buffer etc.)
 - int* start_and_finish_id - variable to store the IDs of start and finish symbols
 - int* line_id - variable to store the ID of course line to draw the fastest route in the end.
 - int* midpoint_id - variable to store the ID of the control point/ midpoint symbol for running through it on the fastest route.
 - int* bridge_id - variable to store the ID of a bridge to ensure we process it individually later.
 - int* start_and_finish_index - variable to store the index of start and finish objects in the list_of_objects
 - int* extremy - variable to store the global extreme x and y values of all objects in the .omap file
 - int* midpoint_index - variable to store the index the midpoint object in the list of objects
 - bool* terminate_program - pointer on a bool in which we store the information if we want to terminate the program (true) or keep going (false)
 - int* start_and_finish_coordinates - variable to store the coordinates of start and finish in the grid scale. [0] - start x, [1] - start y, [2] - finish x, [3] - finish y
 - int* midpoint_coordinates - variable to store the coordinates of the midpoint object on the map, [0] - x, [1] - y
 - int* grid_dimensions - variable to store the size of the grid [0] - number of nodes in x direction (first dimension), [1] - number of nodes in x direction (second dimension)
 - Node*** grid - The 2D set of nodes forming a grid that corresponds to the map. Nodes contain information about the running cost through the corresponding place on the map.
	- It is also the graph that is used for the A* algorithm where the edges are according to the 8-neighborhood. The distances between neighboring nodes are the euclidean distances.





