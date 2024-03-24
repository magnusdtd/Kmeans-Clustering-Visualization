#K_means: Clustering Algorithm
#Kmeans_DV = K_means Data Visualization 
#'Kmeans++ algorithm tìm hiểu thêm
#Note: Chương trình có vài trường hợp algorithm cho kết quả k chính xác

import pygame
from random import randint
import math
from sklearn.cluster import KMeans
pygame.init()
pygame.display.set_caption("Kmeans visualization")
screen = pygame.display.set_mode((1200, 700))
running = True
clock = pygame.time.Clock()
K = 0
points = []
clusters = []
labels = []

#colour
BACKGROUND = (102, 204, 255)
BACKGROUND_PANEL = (249, 255, 230) #yellow
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (147, 153, 35)
PURPLE = (255, 0, 255)
SKY = (0, 255, 255)
ORANGE = (255, 125, 25)
GRAPE = (100, 25, 125)
GRASS = (55, 155, 65)

COLORS = [RED, GREEN, BLUE, YELLOW, PURPLE, SKY, ORANGE, GRAPE, GRASS]

#image
windowIcon = pygame.image.load("resources/icon.png")
pygame.display.set_icon(windowIcon)

#font
font = pygame.font.SysFont("arial", 40)
small_font = pygame.font.SysFont("arial", 20)

def draw_button(text_color, text, button_color, x, y, width, height, align_x, align_y):
    text = font.render(text, True, text_color)
    pygame.draw.rect(screen, button_color, (x, y, width, height), 0, 4)
    screen.blit(text, (x + align_x, y + align_y))

def draw_text(text, color, x, y):
    text = font.render(text, True, color)
    screen.blit(text, (x, y))

def draw_interface():
    #Draw panel
    pygame.draw.rect(screen, BLACK, (50, 50, 700, 500)) #(x, y, lenth, width)
    pygame.draw.rect(screen, BACKGROUND_PANEL, (55, 55, 690, 490))

    #buttom +
    draw_button(WHITE, "+", BLACK, 850, 50, 50, 50, 16, 0)

    #button -
    draw_button(WHITE, "-", BLACK, 950, 50, 50, 50, 19, -3)

    #K value
    draw_text("K = " + str(K), BLACK, 850+225, 47)

    #Button Run
    draw_button(WHITE, "Run", BLACK, 850, 150, 150, 50, 47, 0)

    #Button Random
    draw_button(WHITE, "Random", BLACK, 850, 250, 150, 50, 18, 0)

    #Button Algorithm
    draw_button(WHITE, "Algorithm", BLACK, 850, 450, 150, 50, 8, 0)

    #Button Reset
    draw_button(WHITE, "Reset", BLACK, 850, 550, 150, 50, 31, 0)

def draw_mouse_position():
    if (55 <= mouse_x <= 55 + 690 and 55 <= mouse_y <= 55 + 490):
        text_mouse = small_font.render("(" + str(mouse_x - 55) + "," + str(mouse_y - 55) + ")", True, BLACK)
        screen.blit(text_mouse, (mouse_x + 10, mouse_y - 10))

def draw_points():
    for i in range(len(points)):
        pygame.draw.circle(screen, BLACK, (points[i][0] + 55, points[i][1] + 55), 4)
        if len(labels) == 0:
            pygame.draw.circle(screen, WHITE, (points[i][0] + 55, points[i][1] + 55), 3)
        else:
            pygame.draw.circle(screen, COLORS[labels[i]], (points[i][0] + 55, points[i][1] + 55), 3)

def draw_clusters():
    for i in range(len(clusters)):
        vertices = [(clusters[i][0]+55, clusters[i][1]-5+55), (clusters[i][0]-5+55, clusters[i][1]+5+55), (clusters[i][0]+5+55, clusters[i][1]+5+55)]
        pygame.draw.polygon(screen, COLORS[i], vertices) 

def distance(p1, p2):
    return math.sqrt((p1[0] - p2[0])**2 + (p1[1] - p2[1])**2)

def draw_sum_of_distance():
    sum_of_distance = 0
    if (len(clusters) != 0 and len(labels) != 0):
        for i in range((len(points))):
            sum_of_distance += distance(points[i], clusters[labels[i]])
    draw_text("Sum of distances = " +  str(int(sum_of_distance)), BLACK, 800, 350)

while(running):
    clock.tick(60)
    screen.fill(BACKGROUND)

    mouse_x, mouse_y = pygame.mouse.get_pos()

    draw_interface()
    draw_mouse_position()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            #Create point on panel
            if (55 <= mouse_x <= 55 + 690 and 55 <= mouse_y <= 55 + 490):
                labels = []
                points.append([mouse_x - 55, mouse_y - 55])
            #Change K button +
            if (850 < mouse_x < 900 and 50 < mouse_y < 100):
                if (K < len(COLORS)):
                    K += 1 
            #Change K button -
            if (950 < mouse_x < 1000 and 50 < mouse_y < 100):
                if (K > 0): K -= 1
            #Run button
            if (850 < mouse_x < 850 + 150 and 150 < mouse_y < 150 + 50):
                labels = []
                if len(clusters) == 0: continue
                for p in points:
                    min_dis = distance(clusters[0], p)
                    label = 0
                    for i in range(1, len(clusters)):
                        min_dis = min(min_dis, distance(clusters[i], p))
                        if min_dis == distance(clusters[i], p): 
                            label = clusters.index(clusters[i]) 
                    
                    labels.append(label)

                #Update clusters:
                for i in range(K):
                    sum_x = 0
                    sum_y = 0
                    count = 0
                    for j in range(len(points)):
                        if labels[j] == i:
                            sum_x += points[j][0]
                            sum_y += points[j][1]
                            count += 1
                    if count != 0:
                        clusters[i] = [sum_x/count, sum_y/count]

                print("Press run button")
            #Random button
            if (850 < mouse_x < 850 + 150 and 250 < mouse_y < 250 + 50):
                clusters = []
                labels = []
                for i in range(K):
                    clusters.append([randint(5, 685), randint(5, 485)])
                print("Press random button") 
            #Algorithm button
            if (850 < mouse_x < 850 + 150 and 450 < mouse_y < 450 + 50):
                try:
                    kmeans = KMeans(n_clusters = K).fit(points)
                    labels = kmeans.predict(points)
                    clusters = kmeans.cluster_centers_
                except:
                    print("Error") 
                print("Press Algorithm button")  
            #Reset button   
            if (850 < mouse_x < 850 + 150 and 550 < mouse_y < 550 + 50):
                points = []
                labels = []
                clusters = []
                K = 0
                sum_of_distance = 0
                print("Press Reset button") 
    
    draw_points()
    draw_clusters()
    draw_sum_of_distance()

    pygame.display.flip()

pygame.quit()