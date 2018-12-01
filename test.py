from BoardContent import *
import copy


def formatlist(source,outarr,decorate):
    # print("DECORATE LIST",decorate)
    # temp = []
    # temp1 = []
    # for i in range(1,len(source)):
        # if decorate[i]=="LAST" and decorate[i-1]=="LAST":
            # temp.append(i)
    for i in range(1,len(source)):
        array = []

        for j in range(0,i+1):
            array.append(source[j])
            if source[i] in decorate.keys() and source[i] in array and decorate[source[i]][0]=="END":
                temp = array
                if source[i-1] in decorate.keys() and source[i-1] in array and decorate[source[i-1]][0]=="END":
                    temp.remove(source[i-1])
                    # temp.remove(source[i-2
                    if source[i-2] in decorate.keys() and source[i-2] in array and decorate[source[i-2]][0]=="END":
                        temp.remove(source[i-2])
                        if source[i-3] in decorate.keys() and source[i-3] in array and decorate[source[i-3]][0]=="END":
                            temp.remove(source[i-3])
                            if source[i-4] in decorate.keys() and source[i-4] in array and decorate[source[i-4]][0]=="END":
                                temp.remove(source[i-4])
                                if source[i-5] in decorate.keys() and source[i-5] in array and decorate[source[i-5]][0]=="END":
                                    temp.remove(source[i-5])
                                elif source[i-5] in decorate.keys():
                                      if (decorate[source[i-4]][1] in source[i-5].open_neighbours(decorate[source[i-5]][1])
                                              and decorate[source[i]][1] not in source[i-5].open_neighbours(decorate[source[i-5]][1])):
                                          temp.remove(source[i-5])
                            elif source[i-4] in decorate.keys():
                                  if (decorate[source[i-3]][1] in source[i-4].open_neighbours(decorate[source[i-4]][1])
                                          and decorate[source[i]][1] not in source[i-4].open_neighbours(decorate[source[i-4]][1])):
                                      temp.remove(source[i-4])
                                      if source[i-5] in decorate.keys() and source[i-5] in array and decorate[source[i-5]][0]=="END":
                                          temp.remove(source[i-5])
                                      elif source[i-5] in decorate.keys():
                                            if (decorate[source[i-4]][1] in source[i-4].open_neighbours(decorate[source[i-5]][1])
                                                    and decorate[source[i]][1] not in source[i-5].open_neighbours(decorate[source[i-5]][1])):
                                                temp.remove(source[i-5])
                        elif source[i-3] in decorate.keys():
                            if (decorate[source[i-2]][1] in source[i-3].open_neighbours(decorate[source[i-3]][1])
                                    and decorate[source[i]][1] not in source[i-3].open_neighbours(decorate[source[i-3]][1])):
                                temp.remove(source[i-3])
                            if source[i-4] in decorate.keys() and source[i-4] in array and decorate[source[i-4]][0]=="END":
                                temp.remove(source[i-4])
                                if source[i-5] in decorate.keys() and source[i-5] in array and decorate[source[i-5]][0]=="END":
                                    temp.remove(source[i-5])
                                elif source[i-5] in decorate.keys():
                                      if (decorate[source[i-4]][1] in source[i-5].open_neighbours(decorate[source[i-5]][1])
                                              and decorate[source[i]][1] not in source[i-5].open_neighbours(decorate[source[i-5]][1])):
                                          temp.remove(source[i-5])
                            elif source[i-4] in decorate.keys():
                                  if (decorate[source[i-3]][1] in source[i-4].open_neighbours(decorate[source[i-4]][1])
                                          and decorate[source[i]][1] not in source[i-4].open_neighbours(decorate[source[i-4]][1])):
                                      temp.remove(source[i-4])
                                      if source[i-4] in decorate.keys() and source[i-4] in array and decorate[source[i-4]][0]=="END":
                                          temp.remove(source[i-4])
                                      elif source[i-5] in decorate.keys():
                                            if (decorate[source[i-4]][1] in source[i-5].open_neighbours(decorate[source[i-5]][1])
                                                    and decorate[source[i]][1] not in source[i-5].open_neighbours(decorate[source[i-5]][1])):
                                                temp.remove(source[i-5])
                    elif source[i-2] in decorate.keys():
                        if (decorate[source[i-1]][1] in source[i-2].open_neighbours(decorate[source[i-2]][1])
                                and decorate[source[i]][1] not in source[i-2].open_neighbours(decorate[source[i-2]][1])):
                            temp.remove(source[i-2])
                        if source[i-3] in decorate.keys() and source[i-3] in array and decorate[source[i-3]][0]=="END":
                            temp.remove(source[i-3])
                            if source[i-4] in decorate.keys() and source[i-4] in array and decorate[source[i-4]][0]=="END":
                                temp.remove(source[i-4])
                                if source[i-5] in decorate.keys() and source[i-5] in array and decorate[source[i-5]][0]=="END":
                                    temp.remove(source[i-5])
                                elif source[i-5] in decorate.keys():
                                      if (decorate[source[i-4]][1] in source[i-5].open_neighbours(decorate[source[i-5]][1])
                                              and decorate[source[i]][1] not in source[i-5].open_neighbours(decorate[source[i-5]][1])):
                                          temp.remove(source[i-5])
                            elif source[i-4] in decorate.keys():
                                  if (decorate[source[i-3]][1] in source[i-4].open_neighbours(decorate[source[i-4]][1])
                                          and decorate[source[i]][1] not in source[i-4].open_neighbours(decorate[source[i-4]][1])):
                                      temp.remove(source[i-4])
                                      if source[i-5] in decorate.keys() and source[i-5] in array and decorate[source[i-5]][0]=="END":
                                          temp.remove(source[i-5])
                                      elif source[i-5] in decorate.keys():
                                            if (decorate[source[i-4]][1] in source[i-5].open_neighbours(decorate[source[i-5]][1])
                                                    and decorate[source[i]][1] not in source[i-5].open_neighbours(decorate[source[i-5]][1])):
                                                temp.remove(source[i-5])
                        elif source[i-3] in decorate.keys():
                            if (decorate[source[i-2]][1] in source[i-3].open_neighbours(decorate[source[i-3]][1])
                                    and decorate[source[i]][1] not in source[i-3].open_neighbours(decorate[source[i-3]][1])):
                                temp.remove(source[i-3])
                            if source[i-4] in decorate.keys() and source[i-4] in array and decorate[source[i-4]][0]=="END":
                                temp.remove(source[i-4])
                                if source[i-5] in decorate.keys() and source[i-5] in array and decorate[source[i-5]][0]=="END":
                                    temp.remove(source[i-5])
                                elif source[i-5] in decorate.keys():
                                      if (decorate[source[i-4]][1] in source[i-5].open_neighbours(decorate[source[i-5]][1])
                                              and decorate[source[i]][1] not in source[i-5].open_neighbours(decorate[source[i-5]][1])):
                                          temp.remove(source[i-5])
                            elif source[i-4] in decorate.keys():
                                  if (decorate[source[i-3]][1] in source[i-4].open_neighbours(decorate[source[i-4]][1])
                                          and decorate[source[i]][1] not in source[i-4].open_neighbours(decorate[source[i-4]][1])):
                                      temp.remove(source[i-4])
                                      if source[i-5] in decorate.keys() and source[i-5] in array and decorate[source[i-5]][0]=="END":
                                          temp.remove(source[i-5])
                                      elif source[i-5] in decorate.keys():
                                            if (decorate[source[i-4]][1] in source[i-5].open_neighbours(decorate[source[i-5]][1])
                                                    and decorate[source[i]][1] not in source[i-5].open_neighbours(decorate[source[i-5]][1])):
                                                temp.remove(source[i-5])

                elif source[i-1] in decorate.keys():
                    if source[i-2] in decorate.keys() and source[i-2] in array and decorate[source[i-2]][0]=="END":
                        temp.remove(source[i-2])
                        if source[i-3] in decorate.keys() and source[i-3] in array and decorate[source[i-3]][0]=="END":
                            temp.remove(source[i-3])
                            if source[i-4] in decorate.keys() and source[i-4] in array and decorate[source[i-4]][0]=="END":
                                temp.remove(source[i-4])
                                if source[i-5] in decorate.keys() and source[i-5] in array and decorate[source[i-5]][0]=="END":
                                    temp.remove(source[i-5])
                                elif source[i-5] in decorate.keys():
                                      if (decorate[source[i-4]][1] in source[i-5].open_neighbours(decorate[source[i-5]][1])
                                              and decorate[source[i]][1] not in source[i-5].open_neighbours(decorate[source[i-5]][1])):
                                          temp.remove(source[i-5])
                            elif source[i-4] in decorate.keys():
                                  if (decorate[source[i-3]][1] in source[i-4].open_neighbours(decorate[source[i-4]][1])
                                          and decorate[source[i]][1] not in source[i-4].open_neighbours(decorate[source[i-4]][1])):
                                      temp.remove(source[i-4])
                                      if source[i-5] in decorate.keys() and source[i-5] in array and decorate[source[i-5]][0]=="END":
                                          temp.remove(source[i-5])
                                      elif source[i-5] in decorate.keys():
                                            if (decorate[source[i-4]][1] in source[i-5].open_neighbours(decorate[source[i-5]][1])
                                                    and decorate[source[i]][1] not in source[i-5].open_neighbours(decorate[source[i-5]][1])):
                                                temp.remove(source[i-5])
                        elif source[i-3] in decorate.keys():
                            if (decorate[source[i-2]][1] in source[i-3].open_neighbours(decorate[source[i-3]][1])
                                    and decorate[source[i]][1] not in source[i-3].open_neighbours(decorate[source[i-3]][1])):
                                temp.remove(source[i-3])
                            if source[i-4] in decorate.keys() and source[i-4] in array and decorate[source[i-4]][0]=="END":
                                temp.remove(source[i-4])
                                if source[i-5] in decorate.keys() and source[i-5] in array and decorate[source[i-5]][0]=="END":
                                    temp.remove(source[i-5])
                                elif source[i-5] in decorate.keys():
                                      if (decorate[source[i-4]][1] in source[i-5].open_neighbours(decorate[source[i-5]][1])
                                              and decorate[source[i]][1] not in source[i-5].open_neighbours(decorate[source[i-5]][1])):
                                          temp.remove(source[i-5])
                            elif source[i-4] in decorate.keys():
                                  if (decorate[source[i-3]][1] in source[i-4].open_neighbours(decorate[source[i-4]][1])
                                          and decorate[source[i]][1] not in source[i-4].open_neighbours(decorate[source[i-4]][1])):
                                      temp.remove(source[i-4])
                                      if source[i-5] in decorate.keys() and source[i-5] in array and decorate[source[i-5]][0]=="END":
                                          temp.remove(source[i-5])
                                      elif source[i-5] in decorate.keys():
                                            if (decorate[source[i-4]][1] in source[i-5].open_neighbours(decorate[source[i-5]][1])
                                                    and decorate[source[i]][1] not in source[i-5].open_neighbours(decorate[source[i-5]][1])):
                                                temp.remove(source[i-5])
                    elif source[i-2] in decorate.keys():
                        if (decorate[source[i-1]][1] in source[i-2].open_neighbours(decorate[source[i-2]][1])
                                and decorate[source[i]][1] not in source[i-2].open_neighbours(decorate[source[i-2]][1])):
                            temp.remove(source[i-2])
                        if source[i-3] in decorate.keys() and source[i-3] in array and decorate[source[i-3]][0]=="END":
                            temp.remove(source[i-3])
                            if source[i-4] in decorate.keys() and source[i-4] in array and decorate[source[i-4]][0]=="END":
                                temp.remove(source[i-4])
                                if source[i-5] in decorate.keys() and source[i-5] in array and decorate[source[i-5]][0]=="END":
                                    temp.remove(source[i-5])
                                elif source[i-5] in decorate.keys():
                                      if (decorate[source[i-4]][1] in source[i-5].open_neighbours(decorate[source[i-5]][1])
                                              and decorate[source[i]][1] not in source[i-5].open_neighbours(decorate[source[i-5]][1])):
                                          temp.remove(source[i-5])
                            elif source[i-4] in decorate.keys():
                                  if (decorate[source[i-3]][1] in source[i-4].open_neighbours(decorate[source[i-4]][1])
                                          and decorate[source[i]][1] not in source[i-4].open_neighbours(decorate[source[i-4]][1])):
                                      temp.remove(source[i-4])
                                      if source[i-5] in decorate.keys() and source[i-5] in array and decorate[source[i-5]][0]=="END":
                                          temp.remove(source[i-5])
                                      elif source[i-5] in decorate.keys():
                                            if (decorate[source[i-4]][1] in source[i-5].open_neighbours(decorate[source[i-5]][1])
                                                    and decorate[source[i]][1] not in source[i-5].open_neighbours(decorate[source[i-5]][1])):
                                                temp.remove(source[i-5])
                        elif source[i-3] in decorate.keys():
                            if (decorate[source[i-2]][1] in source[i-3].open_neighbours(decorate[source[i-3]][1])
                                    and decorate[source[i]][1] not in source[i-3].open_neighbours(decorate[source[i-3]][1])):
                                temp.remove(source[i-3])
                            if source[i-4] in decorate.keys() and source[i-4] in array and decorate[source[i-4]][0]=="END":
                                temp.remove(source[i-4])
                                if source[i-5] in decorate.keys() and source[i-5] in array and decorate[source[i-5]][0]=="END":
                                    temp.remove(source[i-5])
                                elif source[i-5] in decorate.keys():
                                      if (decorate[source[i-4]][1] in source[i-5].open_neighbours(decorate[source[i-5]][1])
                                              and decorate[source[i]][1] not in source[i-5].open_neighbours(decorate[source[i-5]][1])):
                                          temp.remove(source[i-5])
                            elif source[i-4] in decorate.keys():
                                  if (decorate[source[i-3]][1] in source[i-4].open_neighbours(decorate[source[i-4]][1])
                                          and decorate[source[i]][1] not in source[i-4].open_neighbours(decorate[source[i-4]][1])):
                                      temp.remove(source[i-4])


                    # if source[i-2] in decorate.keys() and source[i-2] in array:
                        # temp.remove(source[i-2])
                outarr.append(temp)

        outarr.append(array)
    return outarr
