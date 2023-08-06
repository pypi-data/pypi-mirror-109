import sys


 #schema linting methods
def schema_linter(file_source):
  with open(file_source, "r") as outfile:
    lines = outfile.readlines()
  outfile.close()
  lines_to_delete = []
  workaround_query = "WorkaroundForSDLTypeSystem"
  extends_directive = "@extends"
  directive_found_flag = False
  extend_type_query = ['extend', 'type', 'Query']
  apollo_directives_to_check_for = [['directive', '@key(fields', ':', 'String)', 'on', 'OBJECT'], ['directive', '@extends', 'on', 'OBJECT'], 
  ['directive', '@external', 'on', 'FIELD_DEFINITION'], ['directive', '@requires(fields:', 'String)', 'on', 'FIELD_DEFINITION'] ]
  apollo_directives = ["directive @key(fields : String) on OBJECT \n", 
  "directive @extends on OBJECT \n", "directive @external on FIELD_DEFINITION \n", "directive @requires(fields: String) on FIELD_DEFINITION"]
  query_type_found_flag = False
  index = 0
  # see if empty extend query is allowed in schema linter, index should be -1 (line number starts at 0) write to output file next
  for line in lines:
    if workaround_query in line:
     lines_to_delete.append(index)

    for directive in apollo_directives_to_check_for:
      if all(item in line.split() for item in directive):
        lines_to_delete.append(index)

    if extends_directive in line.split() and "OBJECT" not in line.split():
      directive_found_flag = True
    
    if(directive_found_flag):
      lines_to_delete.append(index)
      if "}" in line:
        directive_found_flag = False
    index += 1
  
  lines_to_delete.sort()
  for element in reversed(lines_to_delete):
        del lines[element]
  
  index = 0
  lines_to_delete = []
  # loop again to make sure changes didn't break schema (accomodate for empty query types)
  for line in lines:
    if ('}' in line.split() and query_type_found_flag):
      lines_to_delete.append(index)
      query_type_found_flag = False

    if ('}' not in line.split() and query_type_found_flag):
      query_type_found_flag = False

    if all(item in line.split() for item in extend_type_query):
      query_type_found_flag = True
      lines_to_delete.append(index)
      index += 1
      continue
    index += 1

  lines_to_delete.sort()
  for element in reversed(lines_to_delete):
        del lines[element]
      

  with open("newschema.graphqls", 'w') as outfile:
        outfile.writelines(lines)
        outfile.writelines(apollo_directives)
    


def main():
    if (sys.argv[1] == "-l"):
      file_source = sys.argv[2]
      schema_linter(file_source)

if __name__ == "__main__":
    main()