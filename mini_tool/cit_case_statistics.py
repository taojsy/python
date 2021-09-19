import os
import re
import csv

mailbox_dic = {'zhijiang.shan@nokia-sbell.com':'Shan Zhijiang',
			   'zhaori.deng@nokia-sbell.com':'Deng Zhaori',
			   'gang.ni@nokia-sbell.com':'Ni Gang',
			   'xiubin.qiu@nokia-sbell.com':'Qiu Xiubin',
			   'hefeng-cookie.qu@nokia-sbell.com':'Qu Hefeng',
			   'hongping.rao@nokia-sbell.com':'Rao Hongping',
			   'shubin.ren@nokia-sbell.com':'Ren Shubin',
			   'peng.lin@nokia-sbell.com':'Lin Peng',
			   'chao.5.liu@nokia-sbell.com':'Liu Chao',
			   'rita.feng@nokia-sbell.com':'Feng Rita',
			   'zhiqiang.q2.liu@nokia-sbell.com':'Liu Zhiqiang',
			   'zhong.1.chen@nokia-sbell.com':'Chen Zhong',
			   'chris.l.cao@nokia-sbell.com':'Cao Chris',
			   'eahsuan.xuan@nokia-sbell.com':'Xu Eahsuan',
			   'lijuan.1.wang@nokia-sbell.com':'Wang Lijuan',
			   'winnie.su@nokia-sbell.com':'Su Winnie',
			   'ling.2.zhao@nokia-sbell.com':'Zhao Ling',
			   'huilin.xu@nokia-sbell.com':'Xu Huilin',
			   'wei.7.chen@nokia-sbell.com':'Chen Wei',
			   'jun.tao@nokia-sbell.com':'Tao Jun'}

def cit_case_statistics(dir):
	"""
	check all cases in  robotws5g and statistics record author for each case, finnally output one dictionary of the mapping between case and author

	"""
	# create one empty list to store case and its author, e.g. [{'case': 'Reference_Test_Case_Template.robot', 'author': 'chris.1.cao@nokia-sbell.com'},
	# {'case': 'CLOUD__DEP_vDU_container_cpu_checking__CLI_5GC001642-A.robot','author':'hongping.rao@nokia-sbell.com'}
	case_author_dic_list = []

	for root, ds, fs in os.walk(dir):
		for f in fs:
			# select out all files with postfix .robot
			if os.path.splitext(f)[1] == '.robot':
				# combine to absolute path
				whole_path = os.path.join(root, f)
				print(whole_path)
				with open(whole_path, encoding='utf-8') as robot_file:
					for line in robot_file.readlines():
						# find out the line where author is defined
						if 'author' in line:
							case_author_dic = {}
							try:
								# reg to filter out email address of team member
								s = re.search(r"[a-z]+((.[0-9])*.[a-z]+)*@nokia-sbell.com", line)
								# s.group(0) return string of email address
								print(s.group(0))
								case_author_dic['case'] = f
								case_author_dic['author'] = s.group(0)
								case_author_dic_list.append(case_author_dic)
								# normally there are two places in .robot file have author name, finding out the first one is enough
								break
							# capture the exception that email address doesn't comply with jun.tao@nokia-sbell.com or jun.1.tao@nokia-sbell.com or jun-c.tao@nokia-sbell.com
							except Exception as e:
								print('get author failed: reason={}', format(str(e)))

	print(case_author_dic_list)
	print(len(case_author_dic_list))
	return case_author_dic_list


def save_to_csv(case_author_dic_list):
	"""
	save the mapping of case and author to csv file
	"""
	file = open('cit_case_statistics.csv', 'w', newline='')
	writer = csv.writer(file)
	writer.writerow(['case', 'author'])
	for i in case_author_dic_list:
		# judge expected key is in the dictionary,if yes return 'True'
		if mailbox_dic.__contains__(i['author']) == True:
			writer.writerow([i['case'], mailbox_dic[i['author']]])

	file.close()


def main():
	dir = r"D:\TA5G\robotws5g\testsuite\AIC"
	case_author_dic_list = cit_case_statistics(dir)
	save_to_csv(case_author_dic_list)
	print('please find result in D:\python\helloworld\mini_tool\cit_case_statistics.csv')


if __name__ == '__main__':
	main()

