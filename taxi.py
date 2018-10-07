import numpy as np
import pandas as pd
import random, sys

from h3 import h3

DRIVER_PROP = 0

DRIVER_PROP_PROB = [0.3, 0.1, 0.25, 0.15, 0.2]
TAXI_MOVE_PROB = [0.7, 0.05, 0.05, 0.05, 0.05, 0.05, 0.05]

WINDOWWIDTH = 1000   # 게임화면의 가로크기
WINDOWHEIGHT = 1000  # 게임화면의 세로크기

left_border = -74.2589
bottom_border = 40.4774
right_border = -73.7004
top_border = 40.9176

# h3_address = h3.geo_to_h3(37.3615593, -122.0553238, 5) # lat, lng, hex resolution
# hex_center_coordinates = h3.h3_to_geo(h3_address) # array of [lat, lng]

center_lat = (top_border + bottom_border) / 2  ## Vertical
center_lon = (right_border + left_border) / 2  ## Horizon

lat_div =  WINDOWHEIGHT / (top_border - bottom_border)
lon_div =  WINDOWWIDTH / (right_border - left_border)


def distance(origin, destination):
    lat1, lon1 = origin
    lat2, lon2 = destination
    radius = 6371 # km

    dlat = math.radians(lat2-lat1)
    dlon = math.radians(lon2-lon1)
    a = math.sin(dlat/2) * math.sin(dlat/2) + math.cos(math.radians(lat1)) \
        * math.cos(math.radians(lat2)) * math.sin(dlon/2) * math.sin(dlon/2)
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1-a))
    d = radius * c

    return d ## in km distance


def get_linspace(ori,des,space_num):
    y1, x1 = ori
    y2, x2 = des

    rtn_x_list = list(np.linspace(x1, x2, int(space_num+1)) )
    rtn_y_list = list(np.linspace(y1, y2, int(space_num+1)) )

    return rtn_x_list , rtn_y_list


def return_nearby_coord(h3_address, dist=1):

    ## Get H3-coord then return nearby 6 coord + center - location

    tmp = h3.k_ring_distances(h3_address, dist)
    rtn_list = []

    for item in tmp:
        tmp2 = list(item)
        for item2 in tmp2:
            rtn_list.append(item2)

    return rtn_list


def return_adj_coord(tmp):
    rtn_list = []

    for item in tmp:
        lat, lon = item
        lat_adj = 1000 - (lat - bottom_border) * lat_div
        lon_adj = (lon - left_border) * lon_div
        rtn_list.append([lon_adj, lat_adj])

    return rtn_list



class Taxi:
    def __init__(self, img_on, img_off, crt_pos):
        self.img_on = img_on
        self.img_off = img_off
        self.call_status = False  ## True - Pass - on, False - Call waiting
        self.out_cell_move = False
        self.str_taxi_status = None
        self.crt_pos = crt_pos  ## h3 index
        self.crt_pos_call_data = None
        self.crt_ori = None ## h3 index
        self.crt_des = None ## h3 index
        self.crt_move_stm = 0      ## Start Total mins
        self.crt_move_etm = 0      ## Estimated Arrival Total mins
        self.crt_move_lst_x = 0     ## Moving Sequence List X - longitude
        self.crt_move_lst_y = 0     ## Moving Sequence List Y - Latitude
        #self.crt_move_x = 0
        #self.crt_move_y = 0
        self.crt_move_y, self.crt_move_x = h3.h3_to_geo(self.crt_pos)
        self.crt_move_remain_tm = 0 ##
        self.crt_move_dist = 0
        self.crt_move_eta = 0
        self.crt_moving = False   ## taxi is moving ? true - moving , false -
        self.crt_call_money = 0
        self.taxi_attribute = None ## Taxi property
        self.total_wait_tm = 0       ## Call waiting Time
        self.crt_drive_tm_no_pass = 0  ## Taxi drive to other cell without Pass
        self.total_trip = 0
        self.total_dist = 0
        self.total_money = 0


    def check_taxiloc(self):
        if self.crt_pos == self.crt_des :
            ## If arrived destination
            ## Update
            return True
        else:
            return False

    def update_taxistatus(self, frame):
        ## Taxi Movement Status Update
        ## if check_taxiloc() == True
        ## Update status

        if self.crt_move_remain_tm > 0 :
            self.crt_move_remain_tm = self.crt_move_remain_tm-1

            self.crt_move_x = self.crt_move_lst_x.pop(0)
            self.crt_move_y = self.crt_move_lst_y.pop(0)

            if self.call_status == False:
                self.total_wait_tm = self.total_wait_tm  + 1

        else:
            self.crt_moving = False

        if self.crt_moving == True :

            self.out_cell_move = False
            self.crt_pos = self.crt_des

            if self.call_status == True :
                self.total_trip = self.total_trip + 1
                self.total_money = self.total_money + self.crt_call_money

            self.total_dist = self.total_dist + self.crt_move_dist
            self.call_status = False

            self.crt_ori = None  ## h3 index
            self.crt_des = None  ## h3 index
            self.crt_move_stm = 0  ## Start Total mins   ( Frame )
            self.crt_move_etm = 0  ## Estimated Arrival Total mins  ( Frame )
            self.crt_move_lst_x = 0  ## Moving Sequence List X - longitude
            self.crt_move_lst_y = 0  ## Moving Sequence List Y - Latitude

            self.crt_move_y, self.crt_move_x = h3.h3_to_geo(self.crt_pos)
            #self.crt_move_x = 0
            #self.crt_move_y = 0
            self.crt_move_remain_tm = 0  ##
            self.crt_move_dist = 0
            self.crt_move_eta = 0
            self.crt_call_money = 0


        return 0


    def check_taxigetcall(self, df_call, prob=DRIVER_PROP_PROB):

        ## Within 1 min - All call list
        df_crt_pos = df_call[(df_call['s_loc']==self.crt_pos)]

        ## Driver's call selection attribute
        ## For testing - it set to be randomly selected
        ##
        #driver_prone = self.taxi_attribute

        driver_prone = np.random.choice(np.arange(0, len(prob)), p=prob)

        self.taxi_attribute = driver_prone

        #################
        ## Test Code
        driver_prone = 2

        self.str_taxi_status = 'Get Call'

        if len(df_crt_pos) > 0:
            ## There is a call in crt_pos
            if driver_prone == 0: ## get long dist call
                #idx = df_crt_pos.index[df_crt_pos['h_dist'] == df_crt_pos['h_dist'].max()].tolist()
                df_tmp2 = df_crt_pos[(df_crt_pos['h_dist'] == df_crt_pos['h_dist'].max())]
                #df_tmp2 = df_crt_pos[idx[0]]#[:1]

            if driver_prone == 1: ## get long eta - call
                #idx = df_crt_pos.index[df_crt_pos['eta_mins'] == df_crt_pos['eta_mins'].max()].tolist()
                df_tmp2 = df_crt_pos[(df_crt_pos['eta_mins'] == df_crt_pos['eta_mins'].max())]
                #df_tmp2 = df_crt_pos.iloc[idx, :]#[:1]

            if driver_prone == 2: ## get short dist - call
                #idx = df_crt_pos.index[df_crt_pos['h_dist'] == df_crt_pos['h_dist'].min()].tolist()
                #df_tmp2 = df_crt_pos.iloc[idx, :]#[:1]
                df_tmp2 = df_crt_pos[(df_crt_pos['h_dist'] == df_crt_pos['h_dist'].min())]

            if driver_prone == 3: ## get short eta - call
                #idx = df_crt_pos.index[df_crt_pos['eta_mins'] == df_crt_pos['eta_mins'].min()].tolist()
                #df_tmp2 = df_crt_pos.iloc[idx, :]#[:1]
                df_tmp2 = df_crt_pos[(df_crt_pos['eta_mins'] == df_crt_pos['eta_mins'].min())]

            if driver_prone == 4: ## Waiting
                ## Decide not to take current Call
                ## After This call -> Choosing the Moving Action
                self.check_taximove()
                self.total_wait_tm = self.total_wait_tm + 1
                return False

            ## df_tmp2 - Col list
            ## 0- h_dist,
            ## 1- s_cen_lat
            ## 2- s_cen_lon
            ## 3- e_cen_lat
            ## 4- e_cen_lon
            ## 5- s_mins
            ## 6- e_mins
            ## 7- eta_mins
            ## 8- fare_amount
            ## 9- s_loc
            ##10- e_loc

            self.call_status = True
            self.crt_ori = df_tmp2.iloc[0, 9 ]
            self.crt_des = df_tmp2.iloc[0, 10]

            if self.crt_ori != self.crt_des :
                self.out_cell_move = True
            else:
                self.out_cell_move = False

            self.crt_move_stm = df_tmp2.iloc[0, 5]
            self.crt_move_etm = df_tmp2.iloc[0, 6]
            self.crt_move_remain_tm = df_tmp2.iloc[0, 7]
            self.crt_move_dist = df_tmp2.iloc[0, 0]
            self.crt_move_eta = df_tmp2.iloc[0, 7]
            self.crt_call_money = df_tmp2.iloc[0, 8]

            ori_coords = h3.h3_to_geo(self.crt_ori)
            des_coords = h3.h3_to_geo(self.crt_des)
            self.crt_move_lst_x, self.crt_move_lst_y = get_linspace(ori_coords, des_coords, self.crt_move_remain_tm)

            self.crt_move_x = self.crt_move_lst_x[0]
            self.crt_move_y = self.crt_move_lst_y[0]

            ## Get Call
            return True
        else :
            ## Not Get Call
            ## Waitting until some call is activated in cell
            if self.crt_move_remain_tm == 0:
                self.check_taximove()
            self.total_wait_tm = self.total_wait_tm + 1
            return False


    def check_taximove(self, prob =TAXI_MOVE_PROB ):

        ## When check_taxigetcall return False ->
        ## Decide to wait ( in - cell ) or go out - cell

        ## Decision to wait : selected location = self.crt_pos
        ## Decision to go out - cell : selected location != self.crt_pos

        ## Pre-defined Prob TAXI_MOVE_PROB = [0.7, 0.05, 0.05, 0.05, 0.05, 0.05, 0.05]

        nearby_coord_list = return_nearby_coord(self.crt_pos)

        select_loc = nearby_coord_list[np.random.choice(np.arange(0, len(nearby_coord_list)), p=prob)]

        ## for waiting test
        select_loc = nearby_coord_list[1]

        if select_loc != self.crt_pos:

            ## Out cell move while waiting
            tmp_eta = random.randint(4,6)
            self.str_taxi_status = 'Wait out Move'
            self.out_cell_move = True
            self.crt_ori = self.crt_pos
            self.crt_des = select_loc
            self.crt_move_remain_tm = tmp_eta
            self.crt_move_dist = 1
            self.crt_move_eta = tmp_eta

            ori_coords = h3.h3_to_geo(self.crt_ori)
            des_coords = h3.h3_to_geo(self.crt_des)
            self.crt_move_lst_x, self.crt_move_lst_y = get_linspace(ori_coords, des_coords, self.crt_move_remain_tm)

            self.crt_move_x = self.crt_move_lst_x[0]
            self.crt_move_y = self.crt_move_lst_y[0]

        else:

            ## in - cell waiting
            self.out_cell_move = False
            self.str_taxi_status = 'Wait'

        return 0

    def check_action(self):


        ## Every Frame Set Crt-pos as H3
        self.crt_pos = h3.geo_to_h3(self.crt_move_y, self.crt_move_x, 8)

        ## When Moving -> Moving Taxi 1-frame

        if self.crt_moving == True :
            if self.crt_move_remain_tm > 0 :
                self.crt_move_remain_tm = self.crt_move_remain_tm - 1

                if len(self.crt_move_lst_x)>0:
                    self.crt_move_x = self.crt_move_lst_x.pop(0)

                if len(self.crt_move_lst_y) > 0:
                    self.crt_move_y = self.crt_move_lst_y.pop(0)

            else :
                ## Ariving destination
                self.crt_moving = False

                if self.call_status == True :
                    # If Taxi arrived with passengers
                    self.total_trip = self.total_trip + 1
                    self.total_money = self.total_money + self.crt_call_money
                    self.call_status = False

                self.total_dist = self.total_dist + self.crt_move_dist

                self.crt_ori = None  ## h3 index
                self.crt_des = None  ## h3 index
                self.crt_move_stm = 0  ## Start Total mins   ( Frame )
                self.crt_move_etm = 0  ## Estimated Arrival Total mins  ( Frame )
                self.crt_move_lst_x = 0  ## Moving Sequence List X - longitude
                self.crt_move_lst_y = 0  ## Moving Sequence List Y - Latitude






        ## self.crt_pos_call_data : Crt Loc' Call Dataframe

        df_crt_pos = self.crt_pos_call_data

        if self.call_status == False :
            # Get Call

            driver_prone = np.random.choice(np.arange(0, len(prob)), p=prob)

            self.taxi_attribute = driver_prone

            #################
            ## Test Code
            driver_prone = 2

            self.str_taxi_status = 'Get Call'

            ## Assess the call Attractiveness

            if len(df_crt_pos) > 0:
                ## There is a call in crt_pos
                if driver_prone == 0:  ## get long dist call
                    df_tmp2 = df_crt_pos[(df_crt_pos['h_dist'] == df_crt_pos['h_dist'].max())]

                if driver_prone == 1:  ## get long eta - call
                    df_tmp2 = df_crt_pos[(df_crt_pos['eta_mins'] == df_crt_pos['eta_mins'].max())]

                if driver_prone == 2:  ## get short dist - call
                    df_tmp2 = df_crt_pos[(df_crt_pos['h_dist'] == df_crt_pos['h_dist'].min())]

                if driver_prone == 3:  ## get short eta - call
                    df_tmp2 = df_crt_pos[(df_crt_pos['eta_mins'] == df_crt_pos['eta_mins'].min())]

                if driver_prone == 4:  ## Waiting
                    ## Decide not to take current Call
                    ## After This call -> Choosing the Moving Action
                    self.check_taximove()
                    self.total_wait_tm = self.total_wait_tm + 1
                    return False
        else:




        return 0


    def update_agents(self):

        return 0


    def display_taxiimg(self):
        return 0


    def add(self, num):
        self.result += num
        return self.result