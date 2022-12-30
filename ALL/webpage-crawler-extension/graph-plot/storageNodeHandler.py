# This files contains the logic to handle the storage node in the graph

import json

# storage_dic = {'_gid' = [002, 5288992, 1], '_svd' = [5]}
# script_dic = {'https://ad/test.js': [set->[_gid,..], get->[_svd, ..]]}
def addStorage(script_dic, storage_dic, dataset):
    """
    {"top_level_url":"https://cmovies.online/","function":"cookie_setter","cookie":"__PPU_BACKCLCK_3714332=true; expires=Wed, 16 Feb 2022 19:06:24 GMT; path=/; domain=cmovies.online","stack":"Error\n    at HTMLDocument.set (chrome-extension://pibhebgeoaejhpkdfhfgpmhjnfjefafc/inject.js:39:17)\n    at e.<computed>.<computed> [as saveSessionCustomKey] (https://lurgaimt.net/tag.min.js:1:43145)\n    at https://lurgaimt.net/tag.min.js:1:47814\n    at _ (https://lurgaimt.net/tag.min.js:1:8934)\n    at https://lurgaimt.net/tag.min.js:1:47689\n    at ln (https://lurgaimt.net/tag.min.js:1:48253)\n    at HTMLScriptElement.g (https://cmovies.online/:1630:60191)"}
    """
    """
  {"top_level_url":"https://eus.rubiconproject.com/usync.html?p=btwnex&endpoint=eu","function":"cookie_getter","cookie":"khaos=KZPV8CZP-15-K5E0; audit=1|GRYZojcvauLxCRmi07Abd33bvG56iVGUHpZdkt6wQBl5wrSQggMQUFeGcsFVzcEJPOh1wtc3tgnqFTrNE4+z9kqVaHlG5SlgpmvllXEtYN4=","stack":"Error\n    at HTMLDocument.get (chrome-extension://pibhebgeoaejhpkdfhfgpmhjnfjefafc/inject.js:19:17)\n    at readCookie (https://eus.rubiconproject.com/usync.js:4:1684)\n    at runSyncs (https://eus.rubiconproject.com/usync.js:4:10507)\n    at Image.d.onload (https://eus.rubiconproject.com/usync.js:4:9415)"}
  """
    """
  {"top_level_url":"https://www.forbes.com/","function":"storage_setter","storage":{"keyName":"eclstest","keyValue":"eclstest"},"stack":"Error\n    at window.Storage.setItem (chrome-extension://dpclmdhkoabgdfgpfnijjobmogkfbkpo/inject.js:11:13)\n    at t.value (https://contextual.media.net/dmedianet.js?cid=8CU2T3HV4&https=1:1:79966)\n    at new t (https://contextual.media.net/dmedianet.js?cid=8CU2T3HV4&https=1:1:79722)\n    at Module.<anonymous> (https://contextual.media.net/dmedianet.js?cid=8CU2T3HV4&https=1:1:79645)\n    at n (https://contextual.media.net/dmedianet.js?cid=8CU2T3HV4&https=1:1:10874)\n    at https://contextual.media.net/dmedianet.js?cid=8CU2T3HV4&https=1:1:11666\n    at https://contextual.media.net/dmedianet.js?cid=8CU2T3HV4&https=1:1:11677"}
  """
    """
  {"top_level_url":"https://www.forbes.com/","function":"storage_getter","storage":{"keyName":"mnsbucketExpiryTime"},"stack":"Error\n    at window.Storage.getItem (chrome-extension://dpclmdhkoabgdfgpfnijjobmogkfbkpo/inject.js:31:13)\n    at t.value (https://contextual.media.net/bidexchange.js?cid=8CUX956JU:2:112381)\n    at https://contextual.media.net/bidexchange.js?cid=8CUX956JU:2:581866\n    at t.value (https://contextual.media.net/bidexchange.js?cid=8CUX956JU:2:582010)\n    at t.value (https://contextual.media.net/bidexchange.js?cid=8CUX956JU:2:113067)\n    at new t (https://contextual.media.net/bidexchange.js?cid=8CUX956JU:2:112745)\n    at Object.<anonymous> (https://contextual.media.net/bidexchange.js?cid=8CUX956JU:2:112666)\n    at n (https://contextual.media.net/bidexchange.js?cid=8CUX956JU:2:110)\n    at Object.<anonymous> (https://contextual.media.net/bidexchange.js?cid=8CUX956JU:2:15395)\n    at n (https://contextual.media.net/bidexchange.js?cid=8CUX956JU:2:110)"}
  """

    if dataset["function"] == "cookie_setter":
        if dataset["cookie"] != "":

            if dataset["cookie"].split("=")[0].strip() not in storage_dic.keys():
                storage_dic[dataset["cookie"].split("=")[0].strip()] = []
            if (
                dataset["cookie"].split(";")[0].split("=")[1]
                not in storage_dic[dataset["cookie"].split("=")[0].strip()]
            ):
                storage_dic[dataset["cookie"].split("=")[0].strip()].append(
                    dataset["cookie"].split(";")[0].split("=")[1]
                )

            script_url = getStorageScriptFromStack(dataset["stack"])
            if script_url not in script_dic.keys():
                script_dic[script_url] = [[], []]
            if dataset["cookie"].split("=")[0].strip() not in script_dic[script_url][0]:
                script_dic[script_url][0].append(
                    dataset["cookie"].split("=")[0].strip()
                )

    elif dataset["function"] == "cookie_getter":
        if dataset["cookie"] != "":

            script_url = getStorageScriptFromStack(dataset["stack"])
            lst = dataset["cookie"].split(";")
            for item in lst:
                if item.split("=")[0].strip() not in storage_dic.keys():
                    storage_dic[item.split("=")[0].strip()] = []
                if item.split("=")[1] not in storage_dic[item.split("=")[0].strip()]:
                    storage_dic[item.split("=")[0].strip()].append(item.split("=")[1])

                if script_url not in script_dic.keys():
                    script_dic[script_url] = [[], []]
                if item.split("=")[0].strip() not in script_dic[script_url][1]:
                    script_dic[script_url][1].append(item.split("=")[0].strip())

    else:
        if dataset["storage"] != "":

            script_url = getStorageScriptFromStack(dataset["stack"])
            storage_obj = json.dumps(dataset["storage"])
            storage_obj = json.loads(storage_obj)

            if storage_obj["keyName"] not in storage_dic.keys():
                storage_dic[storage_obj["keyName"]] = []
            if dataset["function"] == "storage_setter":
                if storage_obj["keyValue"] not in storage_dic[storage_obj["keyName"]]:
                    storage_dic[storage_obj["keyName"]].append(storage_obj["keyValue"])

            if script_url not in script_dic.keys():
                script_dic[script_url] = [[], []]

            if dataset["function"] == "storage_setter":
                if storage_obj["keyName"] not in script_dic[script_url][0]:
                    script_dic[script_url][0].append(storage_obj["keyName"])

            if dataset["function"] == "storage_getter":
                if storage_obj["keyName"] not in script_dic[script_url][1]:
                    script_dic[script_url][1].append(storage_obj["keyName"])


# script sample -> at l (https://c.amazon-adsystem.com/aax2/apstag.js:2:1929)
# return https://c.amazon-adsystem.com/aax2/apstag.js
def getStorageScriptFromStack(script):
    try:
        script = script.split("\n")[2]
        script = script.split("(")[
            1
        ]  # https://c.amazon-adsystem.com/aax2/apstag.js:2:1929)
        return "https:" + script.split(":")[1]
    except:
        pass


# see if same storage node is used but small substring is removed
# __mgMuidn == muidn
def getStorageDic(storage_dic, _key):
    for key in storage_dic:
        if _key.lower().strip() in key.lower():
            return key
    storage_dic[_key] = []
    return _key
