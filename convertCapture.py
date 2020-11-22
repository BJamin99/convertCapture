import json
import xml.etree.ElementTree as ET
import os
import sys
os.chdir(sys.path[0])
#input()
def main():
#we need the .capture, .scn, and .cnfg for the session.  These three files should have the same base filename
#just different extensions.  They should also be in a path that is the same as that, but that isn't strictly
#necessary for this so we don't need to enforce it.  The path, and filenames should be of the following format:
#Band/Date/Location, or Band-Date-Location.  But ultimately this is irrelevant to the script, so just ask for
#the base filename and let the user know that it needs to be the same for the .capture, .scn, and .cnfg
    scn = None
    cnfg = None
    capture = None
    fname = None
#    fname = input("What is the name of the .capture file to convert (without .capture): ")
    files = os.listdir()
    for i in files:
      if i[-len('.capture'):] == '.capture':
        fname = i[:-len('.capture')]
        if (fname+'.scn' in files) and (fname+'.cnfg' in files):
          break
        fname = None
      
    if fname == None:
      print("Cannot find a matching .capture, .scn, and .cnfg in the directory.\nPlease ensure the script and the .capture/.scn/.cnfg are in the same directory.")
      input()
      return      
    print("Trying to open " + fname + ".capture, " + fname + ".scn and " + fname + ".cnfg.")
    input()
    with open(fname+".scn","r") as f_scn, open(fname+".cnfg","r") as f_cnfg:
        scn = json.load(f_scn)
        cnfg = json.load(f_cnfg)
    tree = ET.parse(fname+".capture")
    capture = tree.getroot()
    scene={}
    line_info={}
    for i in scn:
        scene[i] = scn[i]
        if i == 'line':
            for l in scene[i]:
                if scene[i][l]['link'] == 1 and scene[i][l]['linkmaster'] == 1:
                    #l_user_suffix = "L"
                    l_user_suffix = ""
                elif scene[i][l]['link'] == 1 and scene[i][l]['linkmaster'] == 0:
                    #l_user_suffix = "R"
                    l_user_suffix = ""
                else:
                    l_user_suffix = ""
                line_info[l] = {'color': scene[i][l]['color'], 'username': scene[i][l]['username'] + l_user_suffix}
            #Now that we've saved the unsigned int version of the color, convert color to the 2's complement signed int version
            if scene[i][l]['color'] > 2**31:
                scene[i][l]['color'] -= 2**32
            if scene[i][l]['aux_asn_flags'] > 2**31:
                scene[i][l]['aux_asn_flags'] -= 2**32
                

    #print(line_info.keys())
    for i in cnfg:
        if i not in scene:
            scene[i] = cnfg[i]

    #if you want to keep all empty tracks, comment out this next for loop.
    for i in capture.findall('AudioTrack'):
        #check for children and if no children remove i
        if len(i.findall('AudioEvent')) == 0:
            capture.remove(i)
            continue
        #convert name of "Track #" to "ch#" so it can be looked up in .scn
        t_name = "ch" + i.attrib['name'].split()[-1]
        #convert scene color to capture color
        s_color = hex(line_info[t_name]['color']).upper()
        t_color = "#"+s_color[-2:]+s_color[-4:-2]+s_color[-6:-4]+s_color[-8:-6]
        i.set('name', line_info[t_name]['username'])
        i.set('color', t_color)
    os.rename(fname+".capture",fname+".capture.orig")
    tree.write(fname+".capture", encoding="UTF-8", xml_declaration=True)
    #print(ET.tostring(capture))
    #input()


    with open(fname+".scene",'w') as f_scene:
        json.dump(scene,f_scene, indent="\t")
    #print(json.dumps(scene,indent=2))
    #now we need to write back the new .capture and the .scene.  Should create an archive
    #of the original files.
    print("Here")

if __name__ == '__main__':
    main()

