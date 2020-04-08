import sys,os,traceback,xlrd
import django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "LVT.settings")
django.setup()
from main.models import Language,Module,Project,Img,Relation
from django.db import transaction
project_root = sys.argv[1]
project_name = sys.argv[2]
multi_list = sys.argv[3]
file_path = sys.argv[4]
multi_list = multi_list.split(',')

with transaction.atomic():
    # 保存点
    save_id = transaction.savepoint()
    try:
        # 修改project表
        project,flag = Project.objects.get_or_create(caption=project_name)
        project_id = project.id
        if file_path != '\\':
            workbook = xlrd.open_workbook(file_path)
            table = workbook.sheets()[0]
            nrows = table.nrows
            language_tab = []
            for x in range(1, nrows):
                row = table.row_values(x)
                language_tab.append(
                    {
                        "target_language": row[1],
                        "abbreviation": row[2],
                        "source_language": row[3]
                    }
                )
            for one in language_tab:
                target_obj,flag = Language.objects.get_or_create(caption=one['target_language'],
                                                             abbreviation=one['abbreviation'])
                if flag:
                    source_obj = Language.objects.get(caption=one['source_language'])
                    Relation.objects.create(source=source_obj,target=target_obj,project_id=project_id)

        for multi_name in multi_list:
            img_root = os.path.join(project_root, project_name, multi_name)
            for target_language in os.listdir(img_root):
                target_obj = Language.objects.get(caption=target_language)
                # source_language_obj = Language.objects.get(source_language__target=target_obj)
                language_root = os.path.join(img_root, target_language)
                if not os.path.isdir(language_root):
                    continue
                for root, dir, file in os.walk(language_root):
                    while True:
                        if 'Thumbs.db' in file:
                            file.remove('Thumbs.db')
                        else:
                            break
                    if file:
                        module_list = root.replace(language_root, '').split('\\')[1:]
                        if len(module_list) == 1:
                            module_name = module_list[0]
                        else:
                            module_name = '_'.join(module_list)
                        Module.objects.get_or_create(caption=module_name)
                        # source_language = source_language_obj.caption
                        module_id = list(Module.objects.filter(caption=module_name).values('id'))[0]['id']
                        language_id = target_obj.id
                        # 列表解析+bulk_create一次保存多条数据
                        img_list = [Img(project_id=project_id, status=1,language_id=language_id, module_id=module_id,
                                        target_img_path=os.path.join(root, one).replace(project_root,'')
                                        ) for one in file]
                        Img.objects.bulk_create(img_list)
    except Exception:
        err = traceback.format_exc()
        with open('imgpath2db_log.txt','a') as f:
            f.write(upload_excel_language)
        # 回滚到保存点
        transaction.savepoint_rollback(save_id)
    # 提交从保存点到当前状态的所有数据库事务操作
    transaction.savepoint_commit(save_id)