from collections import deque
# import matplotlib.pyplot as plt
import statistics
import random
from random import seed

# directory="sample_1"
# filename=directory+'/'+'num_tests.txt'
# with open(filename) as f:
#     num_tests_content=f.readlines()
#     # print(num_tests_content)
# num_tests=int(num_tests_content[0])

seed(1)
class Server():
    def __init__(self, server_id, state="OFF", complete=float('inf'), expires=-1):
        self.server_id = server_id
        self.state = state
        # self.setup_time=setup_time
        self.complete = complete
        self.expires = expires


class Job():
    def __init__(self, arrival_time, service_time, departure_time=-1):
        self.arrival_time = arrival_time
        self.service_time = service_time
        self.departure_time = departure_time


# for i in range(1,num_tests+1):
def simulation_random(i):
    ########random model#########
    arrivals_list = []
    service_list = []
    para_list = []
    index = i
    # open arrival file

    file_arrival = "arrival_" + str(index) + '.txt'
    with open(file_arrival) as f:
        arrival_content = f.readlines()
    # arrival_content = [x.strip() for x in arrival_content]
    while '' in arrival_content:
        arrival_content.remove('')
    arrival_rate = float(arrival_content[0])

    # open service file
    file_service = "service_" + str(index) + '.txt'
    with open(file_service) as f:
        service_content = f.readlines()
    while '' in service_content:
        service_content.remove('')
    service_rate = float(service_content[0])
    # for i in services:
    #     service_list.append(float(i))

    # open para file
    file_para = "para_" + str(index) + '.txt'
    with open(file_para) as f:
        para_content = f.readlines()
    para_content = [x.strip() for x in para_content]
    while '' in para_content:
        para_content.remove('')
    for i in para_content:
        para_list.append(float(i))
    num_server = int(para_list[0])
    setup_time = float(para_list[1])
    Tc = float(para_list[2])
    time_end = float(para_list[3])
    ##process data
    lambd = arrival_rate
    u = service_rate
    # distribution_arrival = []
    next_arrival = 0
    while next_arrival < time_end:
        inter_arrival_time = random.expovariate(lambd)
        # distribution_arrival.append(inter_arrival_time)
        next_arrival = next_arrival + inter_arrival_time
        arrivals_list.append(next_arrival)
    # plt.hist(distribution_arrival, bins=50, edgecolor='k')
    # plt.show()
    for i in range(len(arrivals_list)):
        service_time = 0
        for j in range(3):
            x = random.expovariate(u)
            service_time += x
        service_list.append(service_time)

    # plt.hist(service_list, bins=50, edgecolor='k')
    # plt.show()

    ##bulid dic (key:value)==(arrival,service)
    time_dic = {}
    for i in range(len(arrivals_list)):
        time_dic[arrivals_list[i]] = service_list[i]
        # print(time_dic)

    servers = []
    # servers
    for i in range(1, num_server + 1):
        server_ = Server(server_id=i)
        servers.append(server_)
    # jobs
    jobs = []
    for i in range(len(arrivals_list)):
        job = Job(arrival_time=arrivals_list[i], service_time=service_list[i])
        jobs.append(job)
    # Queue
    Queue = deque()
    for i in arrivals_list:
        Queue.append(i)
    # Dispatcher
    Dispatcher = deque()
    if len(Queue) == 0:
        print("There is no job in the Queue")
        return
    if num_server == 0:
        print("No server")
        return
    # Initialization
    ready_job = Queue.popleft()
    num_off = num_server
    for sr in servers:
        if sr.server_id == 1 and sr.state == "OFF":
            sr.complete = ready_job + setup_time
            sr.state = "SETUP"
            num_off -= 1
    for jb in jobs:
        if jb.arrival_time == ready_job:
            templist = []
            templist.append(jb.arrival_time)
            templist.append(jb.service_time)
            templist.append("MARKED")
            Dispatcher.append(templist)
    # Defined states example 2
    # for sr in servers:
    #     if sr.server_id==1 and sr.state=="OFF":
    #         sr.state="DELAYED-OFF"
    #         sr.expires=20
    #         num_off-=1
    #     if sr.server_id==2 and sr.state=="OFF":
    #         # print(sr.server_id)
    #         sr.state="DELAYED-OFF"
    #         sr.expires=17
    #         num_off-=1
    # for jb in jobs:
    #     if jb.arrival_time==ready_job:
    #         templist=[]
    #         templist.append(jb.arrival_time)
    #         templist.append(jb.service_time)
    #         templist.append("MARKED")
    #         Dispatcher.append(templist)
    # print(Dispatcher)
    # print(num_off)


    # print(ready_job, Dispatcher, end=" ")
    # for sr in servers:
    #     print(sr.state, end=" ")
    # print("")

    while num_off != num_server or len(Dispatcher) != 0 or len(Queue) != 0:
        complete_time = float('inf')
        ready_job = None
        if len(Queue) != 0:
            ready_job = Queue.popleft()
            for jb in jobs:
                if jb.arrival_time==ready_job and jb.departure_time!=-1 and len(Queue)!=0:
                    ready_job=Queue.popleft()

        delayoff_flag = 0
        setup_flag = 0
        for sr in servers:
            if sr.expires > 0:
                delayoff_flag = 1
        for sr in servers:
            if sr.complete < complete_time:
                complete_time = sr.complete

        if delayoff_flag == 0:
            for sr in servers:
                if sr.complete < complete_time:
                    complete_time = sr.complete
            if ready_job:
                if ready_job >= complete_time:
                    Queue.appendleft(ready_job)
                num_off = 0
                for sr in servers:
                    if sr.state == "OFF":
                        num_off += 1
                exist_flag = 0
                for disp in Dispatcher:
                    if disp[0] == ready_job:
                        exist_flag = 1
                for jb in jobs:
                    if jb.departure_time!=-1 and jb.arrival_time==ready_job:
                        exist_flag=1
                if num_off != 0 and exist_flag == 0 and ready_job <= complete_time:
                    for sr in servers:
                        if sr.state == "OFF":
                            sr.complete = ready_job + setup_time
                            sr.state = "SETUP"
                            setup_flag = 1
                            # num_off-=1
                            break
                    for jb in jobs:
                        if jb.arrival_time == ready_job:
                            templist = []
                            templist.append(jb.arrival_time)
                            templist.append(jb.service_time)
                            templist.append("MARKED")
                            Dispatcher.append(templist)
                            break
                num_off = 0
                for sr in servers:
                    if sr.state == "OFF":
                        num_off += 1
                exist_flag = 0
                for disp in Dispatcher:
                    if disp[0] == ready_job:
                        exist_flag = 1
                if num_off == 0 and setup_flag == 0 and exist_flag == 0 and ready_job <= complete_time:

                    for jb in jobs:
                        if jb.arrival_time == ready_job:
                            templist = []
                            templist.append(jb.arrival_time)
                            templist.append(jb.service_time)
                            templist.append("UNMARKED")
                            Dispatcher.append(templist)
                            break
            # print log
            # if ready_job and ready_job < complete_time:
            #     print(ready_job, Dispatcher, end=" ")
            #     for sr in servers:
            #         print(sr.state, end=" ")
            #     print("")
            if ready_job is not None and ready_job == complete_time and len(Dispatcher) == 0:
                for sr in servers:
                    if sr.complete == complete_time:
                        sr.state = "BUSY"
                        sr.complete = sr.complete + time_dic[ready_job]
                        # sr.complete=sr.complete+
                        num_setup = 0
                        for sr in servers:
                            if sr.state == "SETUP":
                                num_setup += 1
                        if len(Dispatcher) == num_setup:
                            for dis in Dispatcher:
                                if dis[2] == "UNMARKED":
                                    dis[2] = "MARKED"
                        if len(Dispatcher) == 0:
                            for sr in servers:
                                if sr.state == "SETUP":
                                    sr.state = "OFF"
                                    sr.complete = float('inf')
                                    num_off += 1
                        break
                for jb in jobs:
                    if jb.arrival_time == ready_job:
                        jb.departure_time = complete_time + time_dic[ready_job]
                        break
            if ready_job is None or ready_job >= complete_time:
                # print("haha")
                if len(Dispatcher) != 0:
                    leave_dispatcher = Dispatcher.popleft()
                    complete_flag = 0
                    for jb in jobs:
                        if jb.arrival_time == leave_dispatcher[0] and jb.departure_time != -1:
                            complete_flag = 1
                    if leave_dispatcher[0] <= complete_time and complete_flag == 0:

                        complete_busy=0
                        for sr in servers:
                            if sr.complete==complete_time and sr.state=="BUSY":
                                complete_busy=1

                        for sr in servers:
                            if complete_busy:
                                if sr.complete==complete_time and sr.state=="BUSY":
                                    sr.state = "BUSY"
                                    sr.complete = sr.complete + leave_dispatcher[1]
                                    num_setup = 0
                                    for sr in servers:
                                        if sr.state == "SETUP":
                                            num_setup += 1
                                    for i in range(num_setup):
                                        if Dispatcher and i < len(Dispatcher):
                                            Dispatcher[i][2] = "MARKED"
                                    if len(Dispatcher) == 0:
                                        for sr in servers:
                                            if sr.state == "SETUP":
                                                sr.state = "OFF"
                                                sr.complete = float('inf')
                                                num_off += 1
                                    break
                            elif sr.complete==complete_time and sr.state=="SETUP":
                                sr.state = "BUSY"
                                sr.complete = sr.complete + leave_dispatcher[1]

                                num_setup = 0
                                for sr in servers:
                                    if sr.state == "SETUP":
                                        num_setup += 1
                                for i in range(num_setup):
                                    if Dispatcher and i < len(Dispatcher):
                                        Dispatcher[i][2] = "MARKED"
                                if len(Dispatcher) == 0:
                                    for sr in servers:
                                        if sr.state == "SETUP":
                                            sr.state = "OFF"
                                            sr.complete = float('inf')
                                            num_off += 1
                                # print log
                                # print(complete_time, Dispatcher,end=" ")
                                # for sr in servers:
                                #     print(sr.state, end=" ")
                                # print("")
                                break
                        for jb in jobs:
                            if jb.arrival_time == leave_dispatcher[0]:
                                jb.departure_time = complete_time + leave_dispatcher[1]
                                break
                    if leave_dispatcher[0] > complete_time:
                        Dispatcher.appendleft(leave_dispatcher)
                        for sr in servers:
                            if sr.complete == complete_time:
                                sr.state = "DELAYED-OFF"
                                sr.expires = complete_time + Tc
                                break

                num_setup = 0
                for sr in servers:
                    if sr.state == "SETUP":
                        num_setup += 1
                if len(Dispatcher) < num_setup:
                    max_setup = 0
                    for sr in servers:
                        if sr.state == "SETUP":
                            if sr.complete > max_setup:
                                max_setup = sr.complete
                    for sr in servers:
                        if sr.state == "SETUP":
                            if sr.complete == max_setup:
                                sr.state = "OFF"
                                sr.complete = float('inf')
                                num_off += 1
                                num_setup -= 1

                # print log
                # print(complete_time, Dispatcher, end=" ")
                # for sr in servers:
                #     print(sr.state, end=" ")
                # print("")


                if ready_job and float(ready_job) > float(complete_time):
                    if len(Dispatcher) == 0:
                        for sr in servers:
                            if sr.state == "BUSY" and sr.complete == complete_time:
                                sr.state = "DELAYED-OFF"
                                sr.complete = float('inf')
                                sr.expires = complete_time + Tc
                if len(Dispatcher) == 0 and ready_job is None:

                    for sr in servers:
                        if sr.state == "SETUP":
                            sr.state = "OFF"
                            sr.complete = float('inf')
                            # sr.expires=-1
                            num_off += 1
                            # num_setup-=1
                    for sr in servers:
                        if sr.state == "BUSY":
                            sr.state = "DELAYED-OFF"
                            sr.expires = sr.complete + Tc
                            # print log
                            # print(sr.complete, Dispatcher, end=" ")
                            # for psr in servers:
                            #     print(psr.state, end=" ")
                            # print("")
                            sr.complete = float('inf')
                num_off = 0
                for sr in servers:
                    if sr.state == "OFF":
                        num_off += 1
                        # print log
                        # print(complete_time, Dispatcher, end=" ")
                        # for sr in servers:
                        #     print(sr.state, end=" ")
                        # print("")

        max_expires = -1

        if delayoff_flag == 1:
            # busy_to_delay_flag=0

            for i in range(num_server):
                if ready_job and ready_job >complete_time:
                    # if len(Dispatcher) == 0:
                        for sr in servers:
                            if sr.state == "BUSY" and sr.complete == complete_time:
                                sr.state = "DELAYED-OFF"
                                sr.complete = float('inf')
                                sr.expires = complete_time + Tc
                                complete_time = float('inf')
                                for sr in servers:
                                    if sr.complete < complete_time:
                                        complete_time = sr.complete
                                break
            continue_flag = 0
            if len(Dispatcher) == 0:
                for sr in servers:
                    if sr.state == "DELAYED-OFF":
                        if ready_job and ready_job > sr.expires:
                            sr.state = "OFF"
                            sr.complete = float('inf')
                            sr.expires = -1
                            continue_flag = 1
                            Queue.appendleft(ready_job)
            if continue_flag:
                continue
            if len(Dispatcher) != 0:
                leave_dispatcher = Dispatcher.popleft()
                for sr in servers:
                    if sr.expires > 0:
                        if sr.expires < leave_dispatcher[0]:
                            sr.state = "OFF"

            num_delay = 0
            for sr in servers:
                if sr.expires > 0:
                    num_delay += 1
            for sr in servers:
                if sr.expires > 0:
                    if sr.expires > max_expires:
                        max_expires = sr.expires
            if ready_job:
                if ready_job >= complete_time:
                    Queue.appendleft(ready_job)
                num_off = 0
                for sr in servers:
                    if sr.state == "OFF":
                        num_off += 1
                if len(Dispatcher) == num_delay and num_off != 0:
                    for sr in servers:
                        if sr.state == "OFF":
                            sr.complete = ready_job + setup_time
                            sr.state = "SETUP"
                            setup_flag = 1
                            break
                    for jb in jobs:
                        if jb.arrival_time == ready_job:
                            templist = []
                            templist.append(jb.arrival_time)
                            templist.append(jb.service_time)
                            templist.append("MARKED")
                            Dispatcher.append(templist)
                num_off = 0
                for sr in servers:
                    if sr.state == "OFF":
                        num_off += 1
                if num_off == 0 and setup_flag == 0 and ready_job < max_expires:
                    for jb in jobs:
                        if jb.arrival_time == ready_job:
                            templist = []
                            templist.append(jb.arrival_time)
                            templist.append(jb.service_time)
                            templist.append("UNMARKED")
                            Dispatcher.append(templist)
                if len(Dispatcher) < num_delay and ready_job <= max_expires:
                    for jb in jobs:
                        if jb.arrival_time == ready_job:
                            templist = []
                            templist.append(jb.arrival_time)
                            templist.append(jb.service_time)
                            templist.append("MARKED")
                            Dispatcher.append(templist)
                            break
                if ready_job > max_expires :
                    for sr in servers:
                        if sr.expires == max_expires:
                            sr.state = "OFF"
                            sr.expires = -1
                            sr.complete = float('inf')
                            Queue.appendleft(ready_job)
                            break

            if len(Dispatcher) != 0 :
                leave_dispatcher = Dispatcher.popleft()
                busy_process=0
                for sr in servers:
                    if sr.complete==leave_dispatcher[0]:
                        busy_process=1
                if busy_process==1:
                    for sr in servers:
                        if sr.complete==leave_dispatcher[0]:
                            sr.state = "BUSY"
                            sr.expires = -1
                            sr.complete = leave_dispatcher[0] + leave_dispatcher[1]
                            break
                    for jb in jobs:
                        if jb.arrival_time == leave_dispatcher[0]:
                            jb.departure_time = leave_dispatcher[0] + leave_dispatcher[1]
                            break
                if busy_process==0:
                    for sr in servers:
                        if sr.expires == max_expires:
                            sr.state = "BUSY"
                            sr.expires = -1
                            sr.complete = leave_dispatcher[0] + leave_dispatcher[1]
                            break

                    for jb in jobs:
                        if jb.arrival_time == leave_dispatcher[0]:

                            jb.departure_time = leave_dispatcher[0] + leave_dispatcher[1]
                            # print log
                            # print(jb.arrival_time, Dispatcher, end=" ")
                            # for psr in servers:
                            #     print(psr.state, end=" ")
                            # print("")

                            break


            if ready_job is None and len(Dispatcher) == 0:

                # print("haha")
                for sr in servers:
                    sr.state="OFF"
                    sr.expires=-1
                    sr.complete=float('inf')
                    # if sr.state == "DELAYED-OFF":
                    #     sr.state = "OFF"

                        #print log
                        # print(sr.expires, Dispatcher, end=" ")
                        # for psr in servers:
                        #     print(psr.state, end=" ")
                        # print("")
                        # sr.expires = -1
                        # sr.complete = float('inf')
            num_off = 0
            for sr in servers:
                if sr.state == "OFF":
                    num_off += 1

    d = {}
    for jb in jobs:
        d[jb.arrival_time] = jb.departure_time

    s = [(k, d[k]) for k in sorted(d, key=d.get, reverse=False)]

    response_time = []
    depature_filename = "departure_" + str(index) + '.txt'
    job_th = 0
    with open(depature_filename, "w") as depature_file:
        for k, v in s:
            job_th += 1
            # if v < time_end and job_th > 1000:
            if v<time_end and v!=-1:
            # if v!=-1:
                response_time.append(v - k)
                depature_file.write("%.3f\t%.3f\n" % (k, v))

    mean_reponse_time = statistics.mean(response_time)
    mrt_filename = "mrt_" + str(index) + '.txt'
    with open(mrt_filename, "w") as mrt_file:
        mrt_file.write("%.3f" % (mean_reponse_time))


    ###plot the graph
    # x_axies=[]
    # y_axies=[]
    # for i in range(1,len(response_time)+1):
    #     x_axies.append(i)
    #     y_axies.append(statistics.mean(response_time[:i]))
    # plt.plot(x_axies,y_axies)
    # plt.ylabel('Mean response time of first k jobs(after transient remove)')
    # plt.xlabel('k')
    # plt.show()

# for i in range(1,2):
#     simulation_trace(i)
