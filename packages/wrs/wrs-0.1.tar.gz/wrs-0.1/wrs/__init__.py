def wr_split(delimeters,text):
  sep,str = delimeters , text
  sep = sep.replace(" ","")
  List = sep.split("|")
  #print(sep,List)

  for i in List:
    replace = True
    while replace == True:
      index = str.find(i)
      str = str[:index] + '| ' + str[index:]
      str = str.replace(i, i.upper(),1)
      if i.lower() not in str:
        replace = False

  str = str.lower()
  text_list = str.split("| ", )

  return text_list
