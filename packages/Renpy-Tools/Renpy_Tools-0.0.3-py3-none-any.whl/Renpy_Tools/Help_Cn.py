#中文帮助

#-h 显示帮助

#-e 选择翻译和注解要被反转的文件
#[例如: Renpy_Tools -e chinese.rpy]

#-r 选择被替换文本的文件
#[例如: Renpy_Tools -r chinese.rpy chinese2.rpy 1]
#文件1:chinese1
#用来获取关键文字的文件
#文件2:chinese2
#根据文件1，替换文件2里的翻译文本

#文本例子：

#    # game/script.rpy:19
#   translate russian start_915cb944:【标签】
#
#        # "It's only when I hear the sounds of shuffling feet and supplies being put away that I realize that the lecture's over."【注解文本】
#        "Только когда я услышал шорох ног и сумок, я понял, что лекция кончилась."  【翻译文本】

#模式:1
#一共用3个模式
#1（默认）：根据文件1里的注解里的文本，并以注解下一行的文本作为翻译文本
#	替换文件2里的对应注解文本的翻译文本
#2：根据文件1里的标签，并以标签以后第三行的文本作为翻译文本
#	替换文本2里对应标签的翻译文本
#3：根据文件1的顺序，依次替换文本2的翻译文本