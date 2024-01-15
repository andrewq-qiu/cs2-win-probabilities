"""A module containing utility functions for use in the scripts."""


def parse_txt_file_list(path: str) -> list[str]:
    """Read filename and return a list of each row, ignoring comments deliminated by #"""
    
    lst = []
    
    with open(path, 'r') as f:
        for row in f:
            pound_loc = row.find('#')
            
            if pound_loc == -1:
                lst.append(row)
            elif pound_loc > 0: # Comment not first character
                lst.append(row[:pound_loc])
                
    return lst