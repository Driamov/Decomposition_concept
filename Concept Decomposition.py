import openai
import networkx as nx
import re
import os
from graphviz import Digraph

os.environ["PATH"] += os.pathsep + "/usr/local/bin"

# Создаем объект Digraph
dot = Digraph('decomposition_graph', format='png', engine='dot')

API_KEY = "XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX"

openai.api_key = API_KEY


# obtaining an elementary decomposition of the concept {text} in the sense of {context}
# decomposition can be direct and reverse - the reverse parameter answers
# decomposition can be obtained via the GPT API or emulated based on advance
# prepared example simul = 1

def get_decomposition_concepts(text, context, simul,revers):
    level_t=[]
    decomp_t=[]
    elem_t="  "

    #  simulation of a three-level direct decomposition of the mobile operator concept
    sm_lvl=[
        [['Mobile operator']],
        [['Mobile operator', 'Network infrastructure', 'Subscriber database', 'Services', 'Tariff plans', 'Billing system']],
        [['Network infrastructure', 'Core network', 'Radio access network', 'Network elements', 'Network management system', 'Interconnection system'],
         ['Subscriber database', 'Subscribers', 'Database'],
         ['Services', 'Network services', 'Mobile data', 'Voice calls', 'Sms', 'Customer service', 'Technical support', 'Billing support'],
         ['Tariff plans', 'Price policy', 'Benefits', 'Payment methods', 'Promotions'],
         ['Billing system', 'Payment processing', 'Customer data', 'Financial reporting', 'Invoicing', 'Billing automation']],
        [['Core network', 'Mobile switching center', 'Base station controller', 'Base transceiver station', 'Home location register', 'Visitor location register'],
         ['Radio access network', 'Base stations', 'Antennas', 'Radio frequency transmission', 'Subscribers equipment', 'Mobile core network'],
         ['Network elements', 'Subscriber data management', 'Radio resource management', 'Mobility management'],
         ['Network management system', 'Network configuration', 'Network monitoring', 'Security management', 'Performance management', 'Fault management'],
         ['Interconnection system', 'Connectivity services', 'Mobile traffic routing', 'Network security'],
         ['Subscribers', 'Mobile users', 'Service contracts', 'Payment plans', 'Billing systems'],
         ['Database', 'Data storage', 'Data tables', 'Data records', 'Database security', 'Database maintenance'],
         ['Network services', 'Voice services', 'Voice calling', 'Voicemail', 'Voice messaging', 'Data services', 'Mobile internet', 'Online payments', 'Mobile tv'],
         ['Mobile data', 'Mobile network', 'Data packages', 'Data traffic', 'Data speed', 'Data plans'],
         ['Voice calls', 'Base station', 'Radio channel', 'Switching center', 'Subscriber line'], ['Sms', 'Short message service', 'Message transfer', 'Network protocol', 'Text message'],
         ['Customer service', 'Call center', 'Online support', 'Quality assurance', 'Customer satisfaction'],
         ['Technical support', 'Technical specialists', 'Troubleshooting', 'Knowledge base'],
         ['Billing support', 'Account management', 'Reporting'], ['Price policy', 'Cost structure', 'Discounts', 'Payment options', 'Promotional offers'],
         ['Benefits', 'Attractive tariffs', 'Quality services', 'Loyalty programs'],
         ['Payment methods', 'Online banking', 'Credit/debit cards', 'Mobile wallet', 'Cashless payments', 'Bank transfer'],
         ['Promotions', 'Advertisements', 'Special offers', 'Promotional campaigns'], ['Payment processing', 'Payment authorization', 'Payment gateway', 'Online payment', 'Credit card processing'],
         ['Customer data', 'Personal information', 'Name', 'Address', 'Phone number', 'Service information', 'Tariff plan', 'Payment history', 'Usage data'],
         ['Financial reporting', 'Financial statements', 'Accounting records', 'Auditing', 'Tax returns', 'Financial analysis'],
         ['Invoicing', 'Invoice creation', 'Financial report'], ['Billing automation', 'Automated billing']
         ]      
    ]

    #  simulation of a three-level inverse decomposition of the concept of a mobile operator in the sense of a market leader     
    sm_lvl_rev=[
        [['Mobile operator']],
        [['Mobile operator', 'Network coverage', 'Quality of service', 'Price plans', 'Customer service', 'Innovative products']],
        [['Network coverage', 'Fast speed', 'Reliable connection', 'Network infrastructure', 'Wide range', 'High capacity', 'Network features', 'Advanced technologies', 'Flexible options', 'Cost efficiency', 'Affordable prices', 'Cost optimization', 'Customer support', 'Professional assistance', 'Prompt response'],
         ['Quality of service', 'Network speed', 'Data security', 'Accessibility'], ['Price plans', 'Network quality', 'Data allowance', 'Call minutes', 'Text messages'],
         ['Customer service', 'Quality products', 'Fast delivery', 'User-friendly app', 'Attentive staff'],
         ['Innovative products', 'Robust technology', 'Comprehensive research', 'Quality customer service', 'Strategic partnerships', 'Cutting-edge design']],
        [['Fast speed', 'Innovative technology', 'High-quality components', 'Comprehensive network coverage', 'Robust infrastructure', 'Advanced features'],
         ['Reliable connection', 'Robust network infrastructure', 'High data speed', 'Stable signal', 'High coverage area', 'Advanced security protocols'],
         ['Network infrastructure', 'High-speed internet', 'Cloud computing', 'Mobile data', 'Network security', 'Data storage'],
         ['Wide range', 'Comprehensive portfolio', 'Robust services', 'Competitive pricing', 'Strong customer base'],
         ['High capacity', 'High-quality products', 'Professional services'],
         ['Network features', 'Coverage', 'Wide area', 'High speed', 'Connectivity', 'Reliable', 'Multifunctional', 'Security', 'Encryption', 'Authentication', 'Mobility', 'Flexible', 'Scalable', 'Quality', 'High performance', 'Low latency'],
         ['Advanced technologies', 'High-quality hardware', 'Innovative software', 'Comprehensive security', 'Advanced networking'],
         ['Flexible options', 'User-friendly interface', 'Customizable options', 'Wide range of products'],
         ['Cost efficiency', 'Strategic planning', 'Market research', 'Competitive analysis', 'Targeting', 'Financial planning', 'Budgeting', 'Cash flow management', 'Business development', 'Product development', 'Innovation', 'Partnerships'],
         ['Affordable prices', 'Quality components', 'Wide selection', 'Efficient delivery'],
         ['Cost optimization', 'Improved efficiency', 'Streamlined processes', 'Automation', 'Resource allocation', 'Re-engineering', 'Cost cutting'],
         ['Customer support', 'Quality assurance', 'Technical assistance', 'User education', 'Problem resolution', 'Customer satisfaction'],
         ['Professional assistance', 'Comprehensive knowledge', 'Expert advice', 'Technical support', 'Onsite services', 'Customized solutions'],
         ['Prompt response', 'Fast customer service', 'Efficient communication', 'Timely feedback', 'Proactive support', 'Immediate issue resolution'],
         ['Network speed', 'Coverage area', 'Network technology', 'Network capacity', 'Data plan', 'Device compatibility'],
         ['Data security', 'Mobile device management', 'Cloud security'], ['Accessibility', 'User experience', 'Ease of use', 'Intuitive interface', 'Responsive design', 'Customization', 'Accessible features'],
         ['Network quality', 'Geographic area', 'Population density', 'Mobile towers', 'Data speed', 'Bandwidth', 'Subscribers', 'Network reliability', 'Uptime', 'Latency', 'Firewalls'],
         ['Data allowance', 'Data packages', 'Free roaming'], ['Call minutes', 'Cost of service', 'Availability of plans'],
         ['Text messages', 'Increased convenience', 'Improved communication', 'Enhanced security', 'Increased customer satisfaction', 'Increased brand awareness'],
         ['Quality products', 'Advanced technology', 'Innovative design', 'Superior materials', 'Customer feedback'],
         ['Fast delivery', 'Convenient delivery options', 'Wide range of delivery services', 'Flexible payment methods', 'Fast and reliable shipping'],
         ['User-friendly app', 'Intuitive design', 'Easy navigation', 'Responsive layout', 'Smooth performance', 'Clear visuals'],
         ['Attentive staff', 'Knowledgeable staff', 'Friendly staff', 'Professional staff', 'Responsive staff', 'Experienced staff'],
         ['Robust technology', 'Scalable architecture', 'Advanced security', 'Reliable performance', 'Flexible customization', 'Comprehensive support'],
         ['Comprehensive research', 'Analyzing customer needs', 'Identifying current market trends', 'Examining competitors', 'Evaluating mobile technologies', 'Investigating user behavior'],
         ['Quality customer service', 'Efficient processes', 'Prompt responses', 'Positive attitude', 'Personalised solutions'],
         ['Strategic partnerships', 'Access to new technologies', 'Expansion of market presence', 'Leverage of resources', 'Cost reduction', 'Risk mitigation'],
         ['Cutting-edge design', 'Personalized content', 'Technology', 'Advanced algorithms', 'Machine learning']
         ]
    ]

    if not simul:
        if revers !=1:
            prompt = f"Cделай декомпозицию понятия {text} в контексте {context}. Результат дай на английском языке в виде двухуровневого ненумерованного списка, где первая строка - декомпозируемое понятие. Понятия должны состоять не менее, чем из двух слов. Количество понятий не более пяти"
        else:
            prompt = f"Назови не менее пяти причин предшествующих понятию {text} в контекстве {context}. Результат дай на английском языке в виде двухуровневого ненумерованного списка, где первая строка - само понятие. Причины должны состоять не менее, чем из двух слов" 
        response = openai.Completion.create(
            engine="text-davinci-003",
            prompt=prompt,
            max_tokens=2048,
            top_p=1.0,
            temperature=0.5,
            n=1,
            stop=None,
            timeout=20,
            best_of=1,
            logprobs=6
        )
        generated_text = response.choices[0].text.strip()
    else:
        generated_text=""
        flag_find=False
        if revers != 1: 
            for level_t in sm_lvl:
                if flag_find:
                    break
                for decomp_t in level_t:
                    if flag_find:
                        break
                    if decomp_t[0]==text and len(decomp_t)!=1:
                        flag_find=True
                        for elem_t in decomp_t:
                            generated_text=generated_text+"\n\t"+elem_t
                        break
        else:    
            for level_t in sm_lvl_rev:
                if flag_find:
                    break
                for decomp_t in level_t:
                    if flag_find:
                        break
                    if decomp_t[0]==text and len(decomp_t)!=1:
                        flag_find=True
                        for elem_t in decomp_t:
                            generated_text=generated_text+"\n\t"+elem_t
                        break 
            
    print("-" * 40)     
    if not simul:
        print("API Response:")
    else:
        print("Simulation Response:")

    print(generated_text)
    print("-" * 40)
    return generated_text


# decomposition request module
# cleaning the response from unnecessary elements
# returns the generated decomposition list, where the first element is the concept text
# being decomposed, and the rest are the decomposition itself

def read_decomp(text, context,simul,revers):
    tmp_lst=[]
    decomposition = get_decomposition_concepts(text, context,simul,revers)
    cleaning_pattern = re.compile(r'^[\s\-*•]+|[\s*:%;,.]+$')
    lines = decomposition.strip().split('\n')
    for line in lines:
        cleaned_line = re.sub(cleaning_pattern,'',line)      
        if cleaned_line:
            cleaned_line = cleaned_line.capitalize()         
            if cleaned_line and any(char.isalpha() for char in cleaned_line):
                cleaned_line = cleaned_line.capitalize()
                tmp_lst.append(cleaned_line)
    return tmp_lst


# module for adding an edge to the visualization graph

def add_edge_to_graph(graph, parent, child, label):
    # Добавьте ребро с меткой между узлами
    graph.edge(parent, child, label)


# module for recursive decomposition of the concept text
# writes nodes and edges to the visualization graph graph_v
# writes decomposition levels to the list of levels all_lvl
# creates a list of all nodes nodes_list
# dept sets the decomposition depth from 0 ....
# simulation - a sign of using a pre-prepared decomposition array
# lvl - the level from which decomposition starts
# reverse - sign of reverse decomposition

def decomp(graph_v,all_lvl,nodes_lst,context, dept, simulation,lvl,revers):

    if dept<=0:
        return
    else: 
        next_lvl=[]                                   # list of next level decompositions
        next_dec=[]                                   # ist of decompositions of the following concept 

        for dec_lvl_lst in all_lvl[lvl:]:             # for all decompositions of the current layer
            for dec_lvl in dec_lvl_lst:     
                if len(dec_lvl)==1:                                                           # if there is only one decomposition in the layer (for example at the start)
                    position=0
                else:
                    position=1
                #print()
                for elem_node in dec_lvl[position:]:                                          # for each concept from the decomposition
                    stop=input("Press any key to continue (Ctrl+C - break)" )
                    tmp_dec=read_decomp(elem_node,context,simulation,revers)                  # We decompose the next concept and save it to a temporary list
                    tmp_lst=[]
                    tmp_lst.append(elem_node)
                    for elem in tmp_dec[1:]:
                        if elem not in nodes_lst:                                              # if the node is not in the list, add it to the graph
                            nodes_lst.append(elem)                                             
                            graph_v.node(elem)                                                 
                            tmp_lst.append(elem)
                            if revers !=1:
                                add_edge_to_graph(graph_v,elem_node,elem,"includes")            # adding an edge to the graph
                                print(tmp_dec[0], "-->",elem)
                            else:
                                add_edge_to_graph(graph_v,elem,elem_node,"includes")            # adding an edge to a graph during inverse decomposition
                                print(elem, "-->",tmp_dec[0])
                    next_dec.append(tmp_lst)
        all_lvl.append(next_dec)
        decomp(graph_v,all_lvl,nodes_lst,context, dept-1, simulation, lvl+1,revers)
  

def main():
    # Creating an Object Digraph
    dot = Digraph(comment='Concept decomposition graph')
    tod = Digraph(comment='Inverse concept decomposition graph')

    # initialization of lists

    all_lvl= []                     
    nodes_lst=[]
    all_lvl_revers=[] 
    nodes_lst_revers=[]

    text = "-"
    context = "-"
    simulatiom=True
    num=1

    print()
    sim=int(input("API or simulation (1/0)?: "))
    if sim==0:
        simulation=True
        text="Mobile operator"
        context="mobile operator structure"
    else:
        simulation=False
        text =input("Enter your concept: ")
        text=text.capitalize()
        context = input("In the context: ")
        context=context.capitalize()
    dept = int(input("Enter the decomposition depth: "))
        
    print()
    nodes_lst.append(text)                      # add the main concept to the list of nodes
    all_lvl.append([[text]])                    # forming a list of levels 
    lvl=0                                       # start with the first layer
    revers=0
    decomp(dot,all_lvl,nodes_lst,context, dept, simulation,lvl,revers)
    print()
    print(all_lvl)

    #visualization of the inverse decomposition graph
    dot.render('decomposition_graph', view=True)

    print()
    print("-------------------  let's do the reverse decomposition  -------------------------")

    text = "-"
    context = "-"
    simulatiom=True
    num=1

    print()
    sim=int(input("API or simulation (1/0)?: "))
    if sim==0:
        simulation=True
        text="Mobile operator"
        context="mobile market leader"
    else:
        text =input("Enter your concept:  ")
        text=text.capitalize()
        context = input("In the context:")
        context=context.capitalize()
        
    dept = int(input("Enter the decomposition depth: "))
   
    print()
    nodes_lst_revers.append(text)
    all_lvl_revers.append([[text]])              
    lvl=0                                        
    revers=1
    decomp(tod,all_lvl_revers,nodes_lst_revers,context, dept, simulation,lvl,revers)
    print()
    print(all_lvl_revers)
        
    # visualization of the inverse decomposition graph
    tod.render('revers_decomposition_graph', view=True)

    
if __name__ == "__main__":
    main()







