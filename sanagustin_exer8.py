# get user input for k
import math
import random
import matplotlib.pyplot as plt
# pip install matplotlib

# get labels of x and y
x_label = ""
y_label = ""

# get number of clusters (k)
while True:
    try:
        k = int(input("Enter number of clusters and centroids: ")) # number of clusters and centroids
        break
    except:
        print("Please enter integers only.")
        
# get user input for columns of data
while True:
    try:
        column1 = int(input("Choose first column [1-14]: "))
        column2 = int(input("Choose second column [1-14]: "))
        if column1 in range(1,15) and column2 in range(1,15) and column1 != column2:
            columns = [column1-1, column2-1] # store column number as index
            break
        else:
            if column1 == column2:
                print("Please choose 2 different columns!")
            else:
                print("Please choose a valid column [1-14].")
    except:
        print("Please choose valid columns [1-14]")
        
# generates random centroid
def getRandomCentroid(length):
    centroid = []
    random_index = random.randint(0, length)
    centroid.append(vector1[random_index])
    centroid.append(vector2[random_index])
    
    return centroid

# computes for the euclidian distance of two points
def getEuclidianDistance(point1, point2):
    sum = 0
    for i in range(2):
        sum += (point2[i] - point1[i])**2
        
    return math.sqrt(sum)
            
# read input from csv file
def getVectors(filename):
    file1 = open(filename, 'r')
    vectors = [] # all vectors/columns will be stored here
    first_vector = []
    second_vector = []
    x = columns[0]
    y = columns[1]
    
    get_label = False
    while True:
        # Get next line from file
        line = file1.readline()
         
        # if line is empty
        # end of file is reached
        if not line:
            break
        
        # split line using comma as delimiter then store each element to vector_v
        vector_v = line.strip().split(",") 
        
        if not get_label:
            global x_label, y_label
            x_label = vector_v[x]
            y_label = vector_v[y]
            get_label = True 
    
        # get elements based on columns chosen by user
        try:
            first_vector.append(float(vector_v[x]))
            second_vector.append(float(vector_v[y])) 
        except:
            continue
    
    file1.close()
    return first_vector, second_vector
        
# maximum of 10 clusters only
if k > 10 or k < 1:
    print("Invalid count of clusters!")
else:
    # read csv file for sample input
    data_set = getVectors("Wine.csv")
    vector1 = data_set[0]
    vector2 = data_set[1]
    
    previous_centroids = [] # list of lists; each list is a coordinate
    current_centroids = []
    
    # generate initial centroids
    for i in range(k):
        # loop until unique centroid is found
        while True:
            centroid = getRandomCentroid(len(vector1))
            if centroid not in current_centroids:
                current_centroids.append(centroid)
                break
            continue
    
    # uncomment this value for checking (works when k = 2)
    # current_centroids.append([2.14, 100])
    # current_centroids.append([2.5, 113])
    
    print("initial", current_centroids)
        
    # dictionary to classify points
    classified_points = {}
    
    # classify points until current centroids matches previous centroids  
    while True:
        # initialize / reset values
        for i in range(k):
            classified_points[i] = [] # initialize list for each centroid
        
        # loop through all the points
        vector_length = len(vector1)
        for i in range(vector_length):
            point = []
            point.append(vector1[i])
            point.append(vector2[i])
            
            point_distances = []
            
            # get the point's euclidian distance from all the centroids
            for j in range(k):
                centroid = current_centroids[j]
                point_distances.append(getEuclidianDistance(point, centroid))
            
            # get the minimum out of all the distances
            min_distance = min(point_distances) 
            min_index = point_distances.index(min_distance)
            classified_points[min_index].append(point)
            
        # save centroid as previous
        previous_centroids = []
        for i in range(k):
            previous_centroids.append(current_centroids[i])
        
        # choose new centroids
        for i in range(k):
            x_sum = 0
            y_sum = 0
            points = classified_points[i] # gets all the points under class i
            class_count = len(points)
            for j in range(len(points)):
                x_sum += points[j][0]
                y_sum += points[j][1]
                
            try:
                new_x = x_sum / class_count
            except:
                new_x = 0
            try:
                new_y = y_sum / class_count
            except:
                new_y = 0
            new_point = [new_x, new_y]
            current_centroids[i] = new_point
        # checks if current centroids matches previous 
        counter = 0
        for i in range(k):
            if current_centroids[i] in previous_centroids:
                counter += 1
                 
        if counter == k:
            break
        
    # print all points
    for i in range(k):
        print(f"centroid {i}: {previous_centroids[i]}")
        points = classified_points[i]
        for j in range(len(points)):
            print(points[j])
            
    # write results to output.csv
    output_file = open("output.csv", "w")
    for i in range(k): 
        string = "Centroid: " + str(i) + " " + str(previous_centroids[i]) + "\n"
        output_file.write(string) # add \n then write to file
        points = classified_points[i]
        for j in range(len(points)):
            string = str(points[j]) + "\n"
            output_file.write(string)
        output_file.write("\n")
    output_file.close()
    
    # plot output
    colors = ["blue", "green", "yellow", "black", "orange", "indigo", "violet", "pink", "cyan", "grey"]
    
    # choose colors
    picked_colors = []
    for i in range(k):
        x_values = []
        y_values = []
        while True:
            index = random.randint(0, 9)
            color = colors[index]
            if color not in picked_colors:
                picked_colors.append(color)
                break
        points = classified_points[i]
        for j in range(len(points)):
            point = points[j]
            x_values.append(point[0]) 
            y_values.append(point[1])
            
        # plot points 
        plt.scatter(x_values, y_values, c=color) 
        
    # add label to x and y
    plt.xlabel(x_label)
    plt.ylabel(y_label)
    plt.title("Kmeans Scatter Plot")
    
    plt.show()