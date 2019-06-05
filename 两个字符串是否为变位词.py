class Anagram:
    """
    @:param s1: The first string
    @:param s2: The second string
    @:return true or false
    """

    # 依次取s1中的字符，每次与s2的副本中的每个字符对比。一个字符找不到即False。
    # 找到后将s2的副本中的对应字符改为None。避免因为有重复字符影响下次比较。
    def Solution1(s1, s2):
        alist = list(s2)

        pos1 = 0
        stillOK = True

        while pos1 < len(s1) and stillOK:
            pos2 = 0
            found = False
            while pos2 < len(alist) and not found:
                if s1[pos1] == alist[pos2]:
                    found = True
                else:
                    pos2 = pos2 + 1

            if found:
                alist[pos2] = None
            else:
                stillOK = False

            pos1 = pos1 + 1

        return stillOK

    print(Solution1('abcd', 'dcba'))

    # 将字符串转为列表后排序，然后依次按位置对比。
    def Solution2(s1, s2):
        alist1 = list(s1)
        alist2 = list(s2)

        alist1.sort()
        alist2.sort()

        pos = 0
        matches = True

        while pos < len(s1) and matches:
            if alist1[pos] == alist2[pos]:
                pos = pos + 1
            else:
                matches = False

        return matches

    print(Solution2('abcde', 'edcbg'))

    # 生成两个26个位置的列表，因为差肯定在26以内。(前提是全小写字母)
    # 求出s1，s2列表中每一个字符与字符'a'ASCII码的差。将其插入到列表中对应差的位置。
    # 因为相同字符的差相同，所以会被插入到两个空列表的相同位置，依次将c1按位置对比即可。
    def Solution3(s1, s2):
        c1 = [0] * 26
        c2 = [0] * 26

        for i in range(len(s1)):
            pos = ord(s1[i]) - ord('a')
            c1[pos] = c1[pos] + 1

        for i in range(len(s2)):
            pos = ord(s2[i]) - ord('a')
            c2[pos] = c2[pos] + 1

        j = 0
        stillOK = True
        while j < 26 and stillOK:
            if c1[j] == c2[j]:
                j = j + 1
            else:
                stillOK = False

        return stillOK

    print(Solution3('apple', 'pleap'))
