import time
import random as r
import functools
import turtle

MAX_X = 500
MAX_Y = 600
DEFAULT_SIZE = 20
SNAKE_SHAPE = 'square'
HIGH_SCORES_FILE_PATH = 'high_scores.txt'
SPEED = 0.1
turtle.addshape('comida.gif')
turtle.addshape('areia.gif')
turtle.addshape('head.gif')
turtle.addshape('cauda.gif')


def load_high_score(state):
    fich = open(HIGH_SCORES_FILE_PATH, 'r')
    state['high_score']=int(fich.readline())    
    fich.close()


def write_high_score_to_file(state):
    fich = open(HIGH_SCORES_FILE_PATH, 'r')
    i = fich.readlines()
    fich.close()
    fich = open(HIGH_SCORES_FILE_PATH, 'w')
    fich.write(str(state['high_score']))
    fich.write('\n')
    fich.writelines(i)
    fich.close()


def create_score_board(state):
    score_board = turtle.Turtle()
    score_board.speed(0)
    score_board.shape("square")
    score_board.color("black")
    score_board.penup()
    score_board.hideturtle()
    score_board.goto(0, MAX_Y / 2.4)
    state['score_board'] = score_board
    load_high_score(state)
    update_score_board(state)

def update_score_board(state):
    state['score_board'].clear()
    state['score_board'].write("Score: {} High Score: {}".format(state['score'], state['high_score']), align="center", font=("Helvetica", 24, "normal"))

def go_up(state):
    if state['snake']['current_direction'] != 'down':
        state['snake']['current_direction'] = 'up'

def go_down(state):
    if state['snake']['current_direction'] != 'up':
        state['snake']['current_direction'] = 'down'

def go_left(state):
    if state['snake']['current_direction'] != 'right':
        state['snake']['current_direction'] = 'left'

def go_right(state):
    if state['snake']['current_direction'] != 'left':
        state['snake']['current_direction'] = 'right'

def init_state():
    state = {}
    state['score_board'] = None
    state['new_high_score'] = False
    state['high_score'] = 0
    state['score'] = 0
    state['food'] = turtle.Turtle()
    state['food'].hideturtle()
    state['food'].color('red')
    state['fundo']=turtle.Turtle()
    state['fundo'].shape('areia.gif')
    state['fundo'].goto(0,0)    
    state['colisao']= turtle.Turtle()
    state['colisao'].hideturtle()
    state['marcacao'] = turtle.Turtle()
    state['marcacao'].hideturtle()
    state['reset']= turtle.Turtle()
    state['reset'].hideturtle() 
    state['window'] = None
    snake = {
        'head': None,    
        'current_direction': None,
        'cauda': []
    }
    state['snake'] = snake
    return state

def setup(state):
    window = turtle.Screen()
    window.setup(width=MAX_X, height=MAX_Y)
    window.listen()
    window.onkey(functools.partial(go_up, state), 'w')
    window.onkey(functools.partial(go_down, state), 's')
    window.onkey(functools.partial(go_left, state), 'a')
    window.onkey(functools.partial(go_right, state), 'd')
    window.tracer(0)
    state['window'] = window
    snake = state['snake']
    snake['current_direction'] = 'stop'
    snake['head'] = turtle.Turtle()
    snake['head'].shapesize()
    snake['head'].shape(SNAKE_SHAPE)
    snake['head'].showturtle()
    snake['head'].pu()
    snake['head'].color('green')
    create_score_board(state)
    create_food(state)
    
    
def marc(state):
    marcacao = state['marcacao'] 
    marcacao.pensize(3)
    marcacao.up()
    marcacao.goto(MAX_X/2,MAX_Y/2)
    marcacao.down()
    marcacao.setheading(-90)
    for i in range(2):
        marcacao.fd(MAX_Y)
        marcacao.right(90)
        marcacao.fd(MAX_X)
        marcacao.right(90)

def move(state):
    snake = state['snake']
    snake['head'].shape('head.gif')
    if snake['current_direction'] == 'up':
        snake['head'].setheading(90)
        snake['head'].fd(DEFAULT_SIZE)  
    if snake['current_direction'] == 'down':
        snake['head'].setheading(-90)
        snake['head'].fd(DEFAULT_SIZE)
    if snake['current_direction'] == 'right':
        snake['head'].setheading(0)
        snake['head'].fd(DEFAULT_SIZE)    
    if snake['current_direction'] == 'left':
        snake['head'].setheading(180)  
        snake['head'].fd(DEFAULT_SIZE)
        
def nova_cauda(state):
    snake=state['snake']
    cauda = turtle.Turtle()
    cauda.shapesize()
    cauda.shape('cauda.gif')
    cauda.showturtle()
    cauda.pu()
    cauda.color('black') 
    snake['cauda'].append(cauda)

def mover_cauda(state):
    snake=state['snake']    
    for i in range(len(snake['cauda'])-1,0,-1):
        snake['cauda'][i].goto(snake['cauda'][i-1].xcor(),snake['cauda'][i-1].ycor())    
    if len(snake['cauda'])>0:
        snake['cauda'][0].goto(snake['head'].xcor(),snake['head'].ycor())    


def create_food(state):
    state['food'].shape('comida.gif')
    snake=state['snake']
    x=r.randint((-MAX_X/2)+10,(MAX_X/2)-10)
    y=r.randint((-MAX_Y/2)+10,(MAX_Y/2)-50)
    x1=[]
    y1=[]
    for i in range(len(snake['cauda'])):
        x1.append(snake['cauda'][i].xcor())
        y1.append(snake['cauda'][i].ycor())
    if (x not in x1) and (y not in y1):
        food = state['food']
        food.goto(x,y)
        food.showturtle()
    else:
        create_food(state)

def check_if_food_to_eat(state):
    food = state['food']
    snake = state['snake']
    state['food'].shape('comida.gif')
    if snake['head'].distance(food.pos()) <= 15:
        food.hideturtle()
        corpo = snake['cauda']
        state['score'] += 10
        create_food(state)
        nova_cauda(state)
        if state['score'] > state['high_score']:
            state['high_score'] = state['score']
            state['new_high_score'] = True
    update_score_board(state)


def boundaries_collision(state):
    snake = state['snake']['head']
    xpos = snake.xcor()
    ypos = snake.ycor()
    if xpos >= MAX_X/2 or xpos <= -MAX_X/2 or ypos <= -MAX_Y/2 or ypos >= MAX_Y/2:
        return True
    
def check_collisions(state):
    snake = state['snake']
    if boundaries_collision(state) == True:
        state['colisao'].write("PERDEU!",align="center", font=("Helvetica", 24, "normal"))
        time.sleep(3)
        state['colisao'].clear()
    for i in snake['cauda']:
        if i.distance(snake['head'])<15:
            state['colisao'].write("BATESTE CONTRA A CAUDA!",align="center", font=("Helvetica", 24, "normal"))
            time.sleep(3)
            state['colisao'].clear()     
            state['reset'].write("O jogo vai ser reiniciado!",align="center", font=("Helvetica", 24, "normal"))
            time.sleep(3)
            turtle.clearscreen()
            if state['new_high_score']:
                write_high_score_to_file(state)
            main()            
            
    return boundaries_collision(state)


def main():
    state = init_state()
    setup(state)
    marc(state)
    while not check_collisions(state):
        state['window'].update()
        check_if_food_to_eat(state)
        mover_cauda(state)
        move(state)
        time.sleep(SPEED)
    state['reset'].write("O jogo vai ser reiniciado!",align="center", font=("Helvetica", 24, "normal"))
    if state['new_high_score']:
        write_high_score_to_file(state)
    time.sleep(3)
    turtle.clearscreen()
    main()
main()