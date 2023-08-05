#!/usr/bin/env python

# Copyright 2017 Earth Sciences Department, BSC-CNS

# This file is part of Autosubmit.

# Autosubmit is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# Autosubmit is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with Autosubmit.  If not, see <http://www.gnu.org/licenses/>.

import networkx
import datetime
import time

from networkx.algorithms.dag import is_directed_acyclic_graph
from networkx import DiGraph
from networkx import dfs_edges
from networkx import NetworkXError


def transitive_reduction(graph):
    try:
        return networkx.algorithms.dag.transitive_reduction(graph)
    except Exception as exp:
        return None
    # if not is_directed_acyclic_graph(graph):
    #     raise NetworkXError("Transitive reduction only uniquely defined on directed acyclic graphs.")
    # reduced_graph = DiGraph()
    # reduced_graph.add_nodes_from(graph.nodes())
    # for u in graph:
    #     u_edges = set(graph[u])
    #     for v in graph[u]:
    #         u_edges -= {y for x, y in dfs_edges(graph, v)}
    #     reduced_graph.add_edges_from((u, v) for v in u_edges)
    # return reduced_graph


class Dependency(object):
    """
    Class to manage the metadata related with a dependency

    """

    def __init__(self, section, distance=None, running=None, sign=None, delay=-1, splits=None, select_chunks=list()):
        self.section = section
        self.distance = distance
        self.running = running
        self.sign = sign
        self.delay = delay
        self.splits = splits
        self.select_chunks_dest = list()
        self.select_chunks_orig = list()
        for chunk_relation in select_chunks:
            self.select_chunks_dest.append(chunk_relation[0])
            if len(chunk_relation) > 1:
                self.select_chunks_orig.append(chunk_relation[1])
            else:
                self.select_chunks_orig.append([])


class SimpleJob(object):
    """
    A simple replacement for jobs
    """

    def __init__(self, name, tmppath, statuscode):
        self.name = name
        self._tmp_path = tmppath
        self.status = statuscode


class SubJob(object):
    """
    Class to manage package times
    """

    def __init__(self, name, package=None, queue=0, run=0, total=0, status="UNKNOWN"):
        self.name = name
        self.package = package
        self.queue = queue
        self.run = run
        self.total = total
        self.status = status
        self.transit = 0
        self.parents = list()
        self.children = list()


class SubJobManager(object):
    """
    Class to manage list of SubJobs
    """

    def __init__(self, subjoblist, job_to_package=None, package_to_jobs=None, current_structure=None):
        self.subjobList = subjoblist
        self.job_to_package = job_to_package
        self.package_to_jobs = package_to_jobs
        self.current_structure = current_structure
        self.subjobindex = dict()
        self.process_index()
        self.process_times()

    def process_index(self):
        for subjob in self.subjobList:
            self.subjobindex[subjob.name] = subjob

    def process_times(self):
        if (self.job_to_package) and (self.package_to_jobs):
            if(self.current_structure) and len(self.current_structure.keys()) > 0:
                new_queues = dict()
                for package in self.package_to_jobs.keys():
                    # print(package)
                    local_structure = dict()
                    local_index = dict()
                    jobs_in_package = filter(lambda x: x.package ==
                                             package, self.subjobList)
                    local_jobs_in_package = [job for job in jobs_in_package]
                    # Build index
                    for sub in local_jobs_in_package:
                        local_index[sub.name] = sub
                    # Build structure
                    for sub in local_jobs_in_package:
                        # sub.parents = list()
                        # sub.children = list()
                        local_structure[sub.name] = [v for v in self.current_structure[sub.name]
                                                     if v in self.package_to_jobs[package]] if sub.name in self.current_structure.keys() else list()

                        sub.children = local_structure[sub.name]
                        # print(sub.children)
                        for child in local_structure[sub.name]:
                            local_index[child].parents.append(sub.name)

                    # Identify roots
                    roots = [sub for sub in local_jobs_in_package if len(
                        sub.parents) == 0]

                    while(len(roots) > 0):
                        sub = roots.pop(0)
                        # print(sub.name)
                        if len(sub.children) > 0:
                            for sub_name in sub.children:
                                if sub_name not in new_queues.keys():
                                    # print(" Adjust " + str(sub_name) + "\t" +
                                    #     str(self.subjobindex[sub_name].queue) + "\t" + str(self.subjobindex[sub.name].queue))
                                    roots.append(local_index[sub_name])
                                    fix = (self.subjobindex[sub_name].queue - (
                                        self.subjobindex[sub.name].queue + self.subjobindex[sub.name].run))
                                    new_queues[sub_name] = fix if fix >= 0 else 0
                                    # print(new_queues[sub_name])

                for key, value in new_queues.items():
                    self.subjobindex[key].queue = value

            else:
                for package in self.package_to_jobs.keys():
                    filtered = filter(lambda x: x.package ==
                                      package, self.subjobList)
                    filtered = sorted(
                        filtered, key=lambda x: x.total, reverse=False)
                    if len(filtered) > 1:
                        temp_index = 0
                        filtered[0].transit = 0
                        for i in range(len(filtered) - 1, 0, -1):
                            # print(i)
                            filtered[i].transit = filtered[i].queue - \
                                filtered[i - 1].total

                        positive = len(
                            [job for job in filtered if job.transit >= 0])

                        if (positive > 1):
                            for i in range(0, len(filtered)):
                                if filtered[i].transit >= 0:
                                    temp_index = i
                                    if i > 0:
                                        filtered[i].queue = (filtered[i].queue -
                                                             filtered[i - 1].total) if (filtered[i].queue -
                                                                                        filtered[i - 1].total) >= 0 else 0
                                else:
                                    filtered[i].queue = (filtered[i].queue -
                                                         filtered[temp_index].total) if (filtered[i].queue -
                                                                                         filtered[temp_index].total) >= 0 else 0
                                # it is starting of level

                    for sub in filtered:
                        self.subjobindex[sub.name].queue = sub.queue
                        # print(sub.name + " in " + sub.package + "\t" + str(sub.total) +
                        #       "\t" + str(sub.queue) + "\t" + str(sub.run) + "\t" + str(sub.transit) + "\t" + str(sub.status))
                    # print("\n")

    def get_subjoblist(self):
        return self.subjobList


def parse_output_number(self, string_number):
    """
    Parses number in format 1.0K 1.0M 1.0G

    :param string_number: String representation of number
    :type string_number: str
    :return: number in float format
    :rtype: float
    """
    number = 0.0
    if (string_number):
        last_letter = string_number.strip()[-1]
        multiplier = 1
        if last_letter == "G":
            multiplier = 1000000000
            number = string_number[:-1]
        elif last_letter == "M":
            multiplier = 1000000
            number = string_number[:-1]
        elif last_letter == "K":
            multiplier = 1000
            number = string_number[:-1]
        else:
            number = string_number
        try:
            number = float(number) * multiplier
        except Exception as exp:
            number = 0.0
            pass
    return number


def job_times_to_text(minutes_queue, minutes_running, status):
    """
    Return text correpsonding to queue and running time
    :param minutes_queue: seconds queuing (actually using seconds)  
    :type minutes_queue: int
    :param minutes_running: seconds running (actually using seconds)  
    :type minutes_running: int
    :param status: current status
    :type status: string
    :return: string
    """
    if status in ["COMPLETED", "FAILED", "RUNNING"]:
        running_text = "( " + str(datetime.timedelta(seconds=minutes_queue)) + \
            " ) + " + \
            str(datetime.timedelta(seconds=minutes_running))
    elif status in ["SUBMITTED", "QUEUING", "HELD", "HOLD"]:
        running_text = "( " + \
            str(datetime.timedelta(seconds=minutes_queue)) + " )"
    elif status in ["NA"]:
        running_text = " <small><i><b>NA</b></i></small>"
    else:
        running_text = ""

    if status == "SUSPICIOUS":
        running_text = running_text + \
            " <small><i><b>SUSPICIOUS</b></i></small>"
    return running_text


def datechunk_to_year(chunk_unit, chunk_size):
    """
    Gets chunk unit and size and returns the value in years

    :return: years  
    :rtype: double
    """
    chunk_size = chunk_size * 1.0
    options = ["year", "month", "day", "hour"]
    if (chunk_unit == "year"):
        return chunk_size
    elif (chunk_unit == "month"):
        return chunk_size / 12
    elif (chunk_unit == "day"):
        return chunk_size / 365
    elif (chunk_unit == "hour"):
        return chunk_size / 8760
    else:
        return 0


def tostamp(string_date):
    """
    String datetime to timestamp
    """
    return int(time.mktime(datetime.datetime.strptime(string_date,
                                                      "%Y-%m-%d %H:%M:%S").timetuple()))


def calculate_SYPD_perjob(chunk_unit, chunk_size, job_chunk, run_time):
    """
    :param chunk_unit: 
    :param chunk_size: 
    :param job_chunk: 
    :param run_time:
    """
    if job_chunk and job_chunk > 0:
        years_per_sim = datechunk_to_year(chunk_unit, chunk_size)
        return round(years_per_sim * 86400 / run_time, 2) if run_time and run_time > 0 else 0
    return None


def calculate_ASYPD_perjob(chunk_unit, chunk_size, job_chunk, queue_run_time, average_post):
    """
    :param chunk_unit: 
    :param chunk_size: 
    :param job_chunk: 
    :param queue_run_time: 
    :param average_post:
    """
    if job_chunk and job_chunk > 0:
        years_per_sim = datechunk_to_year(chunk_unit, chunk_size)
        return round(years_per_sim * 86400.0 / (queue_run_time + average_post), 2) if queue_run_time and average_post and queue_run_time > 0 and average_post > 0 else 0
    return None


def getTitle(job_name, status_color, status_text):
    return job_name + " <span class='badge' style='background-color: " + status_color + "'>#" + status_text + "</span>"
