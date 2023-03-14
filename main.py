
import win32com.client as client
import pathlib
from datetime import date
import datetime as dt
import pyautogui as pg 
from time import sleep

import pandas as pd
from functools import reduce


# Selenium
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys


URL = 'https://sdatool.inc.hp.com/SDA/SDA/Index'

def send_email(file_absolute):
    outlook = client.Dispatch("Outlook.Application")
    message = outlook.CreateItem(0)
    message.To = 'nicolas.papajorge@expeditors.com; guido.camandule@expeditors.com; Hugo.Vignale@expeditors.com; sebastian.smalc@expeditors.com; victoria.monforte@expeditors.com; flor.de.maria.perez@hp.com' 
    message.CC = 'arnol.plazas@hp.com'
    message.Subject = 'SDAs-HTS-ARGENTINA Creados'
    message.Attachments.Add(file_absolute)
    html_body = """
        <html>
            <body>
                <p>Hola, Buen dia a todos</p>
                <br>
                <p>En el documento adjunto se encuentran aquellos casos que ya fueron creados, para su seguimiento.</strong></p>
                <br>
                <p>Saludos<p>
            </body>
        </html>
     """
    message.HTMLBody = html_body
    message.Save()
    message.Send()

def request_sda2(bu, modal, qty, deliveries, delay_reason, delay_subreason, hts_gts, hts_class, sda, invoice):
    print('*' * 100)
    print(invoice)
    print('*' * 100)
    for i in invoice:
            print(i['Invoice_Number'])
            for m in range(0, len(i['Material'])):    
                print(i['Material'][m])
                print(i['QTY'][m])
                print(i['PL'][m])
                print('-' * 100)

def request_sda(bu, modal, qty, deliveries, delay_reason, delay_subreason, hts_gts, hts_class, sda, invoice):
    convert_modal_dict = {'Air': 'Air', 'Ocean': 'Sea', 'Intermodal': 'Sea', 'Truck': 'Road'}
    driver = webdriver.Chrome(executable_path = '../chromedriver.exe')
    driver.maximize_window()
    # driver.get('https://sdatoolitg.inc.hp.com/') # ambiente de prueba
    # driver.get('https://sdatool.inc.hp.com/SDA/SDAOverview/Index')
    driver.get(URL)

    #new_button = WebDriverWait(driver, 80).until(EC.element_located_to_be_selected((By.CLASS_NAME, 'btn-primary btn newSaveRefreshButtonsAlign')))
    #new_button.click()

    sleep(40)
    select_region = Select(WebDriverWait(driver, 30).until(EC.visibility_of_element_located((By.ID, 'drpRegion'))))
    act_options = [option.text for option in select_region.options]   
    select_region.select_by_visible_text('AMS')
    # print(act_options)
    
    select_sub_region =  Select(WebDriverWait(driver, 30).until(EC.visibility_of_element_located((By.ID, 'drpSubRegion'))))
    act_options = [option.text for option in select_sub_region.options] 
    select_sub_region.select_by_visible_text('LAR')
    # print(act_options)

    select_ship_from_country = Select(WebDriverWait(driver, 30).until(EC.visibility_of_element_located((By.ID, 'drpCountry'))))
    act_options = [option.text for option in select_ship_from_country.options] 
    select_ship_from_country.select_by_visible_text('Argentina')
    # print(act_options)

    select_broker = Select(WebDriverWait(driver, 30).until(EC.visibility_of_element_located((By.ID, 'drpSPBroker'))))
    act_options = [option.text for option in select_broker.options] 
    select_broker.select_by_visible_text('AR - Expeditors')
    # print(act_options)

    driver.implicitly_wait(10)
    WebDriverWait(driver, 30).until(EC.visibility_of_element_located((By.XPATH, '//*[@id="koSDADetails"]/div[1]/div[10]/div[2]/span/div/button'))).click()
    driver.implicitly_wait(10)
    
    if bu == 'Printing':
        WebDriverWait(driver, 30).until(EC.visibility_of_element_located((By.XPATH, '//*[@id="koSDADetails"]/div[1]/div[10]/div[2]/span/div/ul/li[2]/a/label/input'))).click() # Imaging And Printing
    else:    
        WebDriverWait(driver, 30).until(EC.visibility_of_element_located((By.XPATH, '//*[@id="koSDADetails"]/div[1]/div[10]/div[2]/span/div/ul/li[1]/a/label/input'))).click() # Personal system
    
    WebDriverWait(driver, 30).until(EC.visibility_of_element_located((By.XPATH, '//*[@id="koSDADetails"]/div[1]/div[10]/div[2]/span/div/button'))).click()
    driver.implicitly_wait(10)

    select_cust_procedure = Select(WebDriverWait(driver, 30).until(EC.visibility_of_element_located((By.ID, 'drpCustomsProc'))))
    act_options = [option.text for option in select_cust_procedure.options] 
    select_cust_procedure.select_by_visible_text('Import')
    # print(act_options)

    select_transport = Select(WebDriverWait(driver, 30).until(EC.visibility_of_element_located((By.ID, 'drpMOT'))))
    act_options = [option.text for option in select_transport.options] 
    select_transport.select_by_visible_text(convert_modal_dict[modal])
    # print(act_options)

    select_ship_from = Select(WebDriverWait(driver, 30).until(EC.visibility_of_element_located((By.ID, 'drpSFC'))))
    act_options = [option.text for option in select_ship_from.options] 
    select_ship_from.select_by_visible_text('Argentina')
    # print(act_options)

    select_ship_to = Select(WebDriverWait(driver, 30).until(EC.visibility_of_element_located((By.ID, 'drpSTC'))))
    act_options = [option.text for option in select_ship_to.options] 
    select_ship_to.select_by_visible_text('Argentina')
    # print(act_options)

    shipment_qty = WebDriverWait(driver, 30).until(EC.visibility_of_element_located((By.ID, 'txtShipments')))
    shipment_qty.send_keys(qty)


    good_description = WebDriverWait(driver, 30).until(EC.visibility_of_element_located((By.ID, 'txtGoodsDesc')))
    good_description.send_keys('Computer equipment')

    btn_save = WebDriverWait(driver, 30).until(EC.visibility_of_element_located((By.ID, 'btnSave')))
    btn_save.click()

    sleep(2)

    
    sda_ticket = WebDriverWait(driver, 30).until(EC.visibility_of_element_located((By.XPATH, '/html/body/div[4]/div/div/div[2]/div')))
    sda_ticket_value = sda_ticket.text[13:]
    pg.press('enter')
    
    sleep(4)
    
    btn_add = WebDriverWait(driver, 30).until(EC.visibility_of_element_located((By.ID, 'addButtonRF')))
    btn_add.click()
    sleep(2)

    reference_number = WebDriverWait(driver, 30).until(EC.visibility_of_element_located((By.ID, 'txtRefNum')))
    for d in deliveries:
        reference_number.send_keys(d, '\n')

    select_reference_type = Select(WebDriverWait(driver, 30).until(EC.visibility_of_element_located((By.ID, 'drpRefType'))))
    act_options = [option.text for option in select_reference_type.options] 
    select_reference_type.select_by_visible_text('Delivery')
    # print(act_options)


    btn_save_reference = WebDriverWait(driver, 30).until(EC.visibility_of_element_located((By.XPATH, '//*[@id="referenceNumberModal"]/div/div/div[2]/div/button[2]')))
    btn_save_reference.click()

    sleep(10)

    btn_delay_reason = WebDriverWait(driver, 30).until(EC.visibility_of_element_located((By.ID, 'btnaddDR')))
    btn_delay_reason.click()

    sleep(5)

    select_delay_reason = Select(WebDriverWait(driver, 30).until(EC.visibility_of_element_located((By.ID, 'drpReason'))))
    act_options = [option.text for option in select_delay_reason.options]   
    select_delay_reason.select_by_visible_text(delay_reason)
    # print(act_options)

    select_delay_subreason = Select(WebDriverWait(driver, 30).until(EC.visibility_of_element_located((By.ID, 'drpSubReason'))))
    act_options = [option.text for option in select_delay_subreason.options] 
    select_delay_subreason.select_by_visible_text(delay_subreason)
    # print(act_options)


    comments_delay_reason = WebDriverWait(driver, 30).until(EC.visibility_of_element_located((By.ID, 'txtComments')))

    comments_delay_reason.send_keys('HTS_GTS   ')
    comments_delay_reason.send_keys('HTS_WWClass   ')
    comments_delay_reason.send_keys('SDA   ')
    comments_delay_reason.send_keys(Keys.ENTER)


    for i, j, k in zip(hts_gts, hts_class, sda):
        comments_delay_reason.send_keys(i)
        comments_delay_reason.send_keys('   ')
        comments_delay_reason.send_keys(j)
        comments_delay_reason.send_keys('   ')
        comments_delay_reason.send_keys(k)
        comments_delay_reason.send_keys(Keys.ENTER)

    
    btn_save_daley_reason = WebDriverWait(driver, 30).until(EC.visibility_of_element_located((By.ID, 'btnSaveDR')))
    driver.implicitly_wait(10)
    ActionChains(driver).move_to_element(btn_save_daley_reason).click(btn_save_daley_reason).perform()

    
    sleep(10)

    btn_add_invoice = WebDriverWait(driver, 30).until(EC.element_to_be_clickable((By.XPATH, '/html/body/div[3]/div[2]/div[6]/table/tbody/tr/td[7]/center/button')))
    btn_add_invoice.click()

    sleep(6)
    driver.switch_to.window(driver.window_handles[1])

    deliveries_uniques = list(set(deliveries))
    if len(invoice) != 0:
        f = 1   
        for i in invoice:
            sleep(6)
            invoice_number = WebDriverWait(driver, 30).until(EC.visibility_of_element_located((By.ID, 'invoiceNumber')))
            invoice_number.send_keys(i['Invoice_Number'])

            select_invoice_type = Select(WebDriverWait(driver, 30).until(EC.visibility_of_element_located((By.ID, 'invoiceTypeAdd')))) 
            select_invoice_type.select_by_visible_text('GTS web portal')
            add_invoice = WebDriverWait(driver, 30).until(EC.element_to_be_clickable((By.XPATH, '/html/body/div[3]/div[3]/div[1]/div/div[2]/div[3]/div[6]/button')))
            add_invoice.click()
            
            if f == 0:
                xpath_details = '/html/body/div[3]/div[3]/div[1]/div/div[2]/div[5]/table/tbody/tr/td[5]/button'
            
            else:
                xpath_details = '/html/body/div[3]/div[3]/div[1]/div/div[2]/div[5]/table/tbody/tr[' + str(f) +']/td[5]/button'
            f+=1

            btn_details = WebDriverWait(driver, 30).until(EC.visibility_of_element_located((By.XPATH, xpath_details))) 
            # ActionChains(driver).move_to_element(btn_details).click(btn_save_daley_reason).perform()
            btn_details.click()
            sleep(5)

            line = 1

            for m in range(0, len(i['Material'])):    
                line_item = WebDriverWait(driver, 30).until(EC.visibility_of_element_located((By.ID, 'lineItemDet')))
                line_item.send_keys(str(line))
                
                product_number = WebDriverWait(driver, 30).until(EC.visibility_of_element_located((By.ID, 'productNumberDet')))
                product_number.send_keys(i['Material'][m])

                qty_pn = WebDriverWait(driver, 30).until(EC.visibility_of_element_located((By.ID, 'qtyDet')))
                qty_pn.send_keys(i['QTY'][m])

                product_line = WebDriverWait(driver, 30).until(EC.visibility_of_element_located((By.ID, 'productLineDet')))
                product_line.send_keys(i['PL'][m])

                add_product_number = WebDriverWait(driver, 30).until(EC.visibility_of_element_located((By.XPATH, '/html/body/div[3]/div[4]/div[1]/div/div[2]/div/div[1]/div[2]/div/div[3]/div[11]/button'))) 
                add_product_number.click()
            
                line += 1
            btn_submit_details = WebDriverWait(driver, 30).until(EC.visibility_of_element_located((By.XPATH, '/html/body/div[3]/div[4]/div[1]/div/div[3]/input[1]')))
            ActionChains(driver).move_to_element(btn_submit_details).click(btn_submit_details).perform()
    else:
        for i in deliveries_uniques:
            invoice_number = WebDriverWait(driver, 30).until(EC.visibility_of_element_located((By.ID, 'invoiceNumber')))
            invoice_number.send_keys(i)

            select_invoice_type = Select(WebDriverWait(driver, 30).until(EC.visibility_of_element_located((By.ID, 'invoiceTypeAdd')))) 
            select_invoice_type.select_by_visible_text('GTS web portal')
            add_invoice = WebDriverWait(driver, 30).until(EC.visibility_of_element_located((By.XPATH, '/html/body/div[3]/div[3]/div[1]/div/div[2]/div[3]/div[6]/button')))
            add_invoice.click()
            sleep(3)
    
    sleep(3)
    driver.quit()

    sda_ticket_value_list = list()
    for i in deliveries_uniques:
        sda_ticket_value_list.append(sda_ticket_value)

    return sda_ticket_value_list


def run():
    today = date.today() - dt.timedelta(days=0)
    today = today.strftime('%d-%m-%Y')
    df_sda = pd.read_excel('./db/Sdas_HTS_AR.xlsx')
    df_sda = df_sda.convert_dtypes()
    
    df_sda.dropna(how='all', inplace=True)
    df_sda = df_sda.astype('string')
    df_sda = df_sda[df_sda['SDA'] != 'Zero Value']
    df_sda.fillna('-', inplace=True)
    df_sda.loc[(df_sda['Mode'] == '-') , 'Mode'] = 'Ocean'
    df_sda['Invoice_Number'] = df_sda['Invoice_Number'].apply(lambda x: x[:-2] if x[-2:] == '.0' else x)
    df_sda_tickets_historical = pd.read_excel('./db/df_sda_tickets_argentina.xlsx')
    df_sda_tickets_historical = df_sda_tickets_historical.convert_dtypes()
    df_sda_tickets_historical = df_sda_tickets_historical.astype('string')

    df_sda = df_sda.merge(df_sda_tickets_historical[['Delivery', 'SDA Number']], on='Delivery', how= 'left')
    df_sda = df_sda[df_sda['SDA Number'].isnull()]
    df_sda.drop(columns=['SDA Number'], inplace=True)


    df_sda = df_sda.loc[:, ['Delivery', 'Material', 'QTY', 'Invoice_Number', 'HTS_GTS', 'HTS_WWClass', 'SDA', 'Mode', 'PL', 'BU']]
    df_delay_reason = pd.read_excel('./db/Delay_reasons.xlsx')

    df_sda = df_sda.merge(df_delay_reason, on='SDA', how='inner')
    df_sda['key'] = df_sda['SDA'] + df_sda['Mode'] + df_sda['BU']
    list_sda = list(df_sda['key'].unique())

    dict_sda = {}
    invoice = {}
    invoices = []
    list_request_sda = []
    for k in list_sda:
        dict_sda.clear()
        df_sda_filter = df_sda[df_sda['key'] == k]
        dict_sda['Delivery']  = list(df_sda_filter['Delivery'])
        dict_sda['QTY'] = list(df_sda_filter['QTY'])
        if k.startswith('Missing Invoice on GTS Report'):
            dict_sda['invoice'] = list()
        else:
            for i in list(df_sda_filter['Invoice_Number'].unique()):
                invoice.clear()
                df_sda_filter_invoice = df_sda_filter[df_sda_filter['Invoice_Number'] == i]
                invoice['Invoice_Number'] = i
                invoice['Material'] = list(df_sda_filter_invoice['Material'])
                invoice['QTY'] = list(df_sda_filter_invoice['QTY'])
                invoice['PL'] = list(df_sda_filter_invoice['PL'])
                invoices.append(invoice.copy())          
            dict_sda['invoice'] = invoices
        dict_sda['HTS_GTS'] = list(df_sda_filter['HTS_GTS'])
        dict_sda['HTS_WWClass'] = list(df_sda_filter['HTS_WWClass'])
        dict_sda['SDA'] = list(df_sda_filter['SDA'].drop_duplicates())
        dict_sda['Mode'] = list(df_sda_filter['Mode'].drop_duplicates())
        dict_sda['BU'] = list(df_sda_filter['BU'].drop_duplicates())
        dict_sda['Delay reason'] = list(df_sda_filter['Delay reason'].drop_duplicates())
        dict_sda['Delay Sub-reason'] = list(df_sda_filter['Delay Sub-reason'].drop_duplicates())
        list_request_sda.append(dict_sda.copy())


    df_sda_tickets = pd.DataFrame()
    print(list_request_sda)
    
    for k in range(0, len(list_request_sda)):
        qty = reduce(lambda a, b: int(a) + int(b), list_request_sda[k]['QTY'])
        qty = str(qty)

        sda_ticket_value = request_sda2(list_request_sda[k]['BU'][0], list_request_sda[k]['Mode'][0], qty, list_request_sda[k]['Delivery'], list_request_sda[k]['Delay reason'][0], list_request_sda[k]['Delay Sub-reason'][0], list_request_sda[k]['HTS_GTS'], list_request_sda[k]['HTS_WWClass'], list_request_sda[k]['SDA'], list_request_sda[k]['invoice'])
        
        # sda_ticket_value = request_sda(list_request_sda[k]['BU'][0], list_request_sda[k]['Mode'][0], qty, list_request_sda[k]['Delivery'], list_request_sda[k]['Delay reason'][0], list_request_sda[k]['Delay Sub-reason'][0], list_request_sda[k]['HTS_GTS'], list_request_sda[k]['HTS_WWClass'], list_request_sda[k]['SDA'], list_request_sda[k]['invoice'])

        # deliveries = list(set(list_request_sda[k]['Delivery']))
        # sdas = list_request_sda[k]['SDA'] * len(deliveries)
        # d = {'Delivery': deliveries, 'SDA': sdas, 'SDA Number': sda_ticket_value, 'Created date': today}
        
        # df_d = pd.DataFrame(data = d)
        # df_sda_tickets_historical = pd.concat([df_sda_tickets_historical, df_d])
        # df_sda_tickets_historical.to_excel('./db/df_sda_tickets_argentina.xlsx', index=False)
    


if __name__ == '__main__':
    run()