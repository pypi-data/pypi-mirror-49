from .mail import Mail
import json

class MAILSend:
    '''
    @set vars start
    '''
    def __init__(self, configs):
        '''
        Submail mail appid
        @type string
        '''
        self.appid = configs['appid']

        '''
        Submail mail appkey
        @type string
        '''
        self.appkey = configs['appkey']

        '''
        sign type (Optional)
        @options: normal or md5 or sha1
        '''
        self.sign_type = ''
        if 'sign_type' in configs:
            self.sign_type = configs['sign_type']

        '''
        to: email recipient
        @array to rfc 822
        '''
        self.to = []

        '''
        add email recipient from addressbook
        @array to string
        '''
        self.address_book = []

        '''
        Sender email
        @type email
        '''
        self.from_ = ''

        '''
        Sender display name
        @type string
        '''
        self.from_name = ''

        '''
        Sender reply email
        @type email
        '''
        self.reply = ''

        '''
        cc recipient email
        @array to string
        '''
        self.cc = []
        
        '''
        bcc recipient email
        @array to string
        '''
        self.bcc = []

        '''
        the email subject
        @string
        '''
        self.subject = ''

        '''
        email text contents
        @mime type:text/plain
        '''
        self.text = ''

        '''
        email html contents
        @mime type:text/html
        '''
        self.html = ''

        '''
        vars: the submail email text content filter
        @type array to json string
        '''
        self.vars = {}

        '''
        links: the submail email links content filter
        @type array to json string
        '''
        self.links = {}

        '''
        attachment
        @type file path, do not add '@'
        '''
        self.attachments = []

        '''
        email headers
        @type  array to json string
        '''
        self.headers = []
    
    '''
    addTo function
    set email and name to array
    '''
    def add_to(self, address, name=''):
        self.to.append({'address':address, 'name':name})

    '''
    AddAddressbook function
    set addressbook sign to array
    '''
    def add_address_book(self,address_book):
        self.address_book.append(address_book)

    '''
    setSender function
    set From and From_name
    '''
    def set_sender(self,sender,name=''):
        self.from_ = sender
        self.from_name = name

    '''
    SetReply function
    set Reply address
    '''
    def set_reply(self, reply):
        self.reply = reply

    '''
    AddCc function
    set cc recipient to array
    '''
    def add_cc(self, address, name=''):
        self.cc.append({'address':address, 'name':name})

    '''
    AddBcc function
    set bcc recipient to array
    '''
    def add_bcc(self, address, name=''):
        self.bcc.append({'address':address, 'name':name})
    
    '''
    Set email subject
    '''
    def set_subject(self, subject):
        self.subject = subject

    '''
    Set email text content
    '''
    def set_text(self, text):
        self.text = text

    '''
    Set email html content
    '''
    def set_html(self, html):
        self.html = html

    '''
    AddVar function
    set var to array
    '''
    def add_var(self, key, val):
        self.vars[key] = val

    '''
    AddLink function
    set link var to array
    '''
    def add_link(self, key, val):
        self.links[key] = val
    
    '''
    AddAttachment function
    set attachment to array
    '''
    def add_attachment(self, attachment):
        self.attachments.append(attachment)

    '''
    AddHeaders function
    set headers to array
    '''
    def add_header(self, key, val):
        self.headers[key] = val

    '''
    build request array
    '''
    def build_request(self):
        request = {}
        '''
        convert To array to rfc 822 format
        '''
        if len(self.to) != 0:
            request['to'] = ''
            for to in self.to:
                request['to'] += to['name']+'<'+to['address']+'>,'
            request['to'] = request['to'][:-1]
        
        '''
        convert Addressbook array to string
        '''
        if len(self.address_book) != 0:
            request['addressbook'] = ''
            for address_book in self.address_book:
                request['addressbook'] += address_book+','
            request['addressbook'] = request['addressbook'][:-1]

        '''
        set sender email
        '''
        request['from'] = self.from_

        '''
        set sender display name, if is not empty
        '''
        if self.from_name != '':
            request['from_name'] = self.from_name

        '''
        set sender reply email, if is not empty
        '''
        if self.reply != '':
            request['reply'] = self.reply

        '''
        convert Cc array to rfc 822 format, if is not empty
        '''
        if len(self.cc) != 0:
            request['cc'] = ''
            for cc in self.cc:
                request['cc'] += cc['name']+'<'+cc['address']+'>,'
            request['cc'] = request['cc'][:-1]

        '''
        convert Bcc array to rfc 822 format, if is not empty
        '''
        if len(self.bcc) != 0:
            request['bcc'] = ''
            for bcc in self.bcc:
                request['bcc'] += bcc['name']+'<'+bcc['address']+'>,'
            request['bcc'] = request['bcc'][:-1]

        '''
        set email subject
        '''
        request['subject'] = self.subject

        '''
        set email text content, if is not empty
        '''
        if self.text != '':
            request['text'] = self.text

        '''
        set email html content, if is not empty
        '''
        if self.html != '':
            request['html'] = self.html

        '''
        convert vars array to json string, if is not empty
        '''
        if len(self.vars) != 0:
            request['vars'] = json.dump(self.vars)

        '''
        convert links array to json string, if is not empty
        '''
        if len(self.links) != 0:
            request['links'] = json.dumps(self.links)

        '''
        convert Attachments array to file upload arrary, if is not empty
        '''
        if len(self.attachments) != 0:
            idx = 0
            for attachment in self.attachments:
                request['attachments[%d'%idx+']'] = "@"+attachment
                idx += 1

        '''
        convert Headers array to json string, if is not empty
        '''
        if len(self.headers) != 0:
            request['headers'] = json.dumps(self.headers)
        return request

    '''
    send email
    '''
    def send(self):
        mail_configs = {}
        '''
        set appid and appkey
        '''
        mail_configs['appid'] = self.appid
        mail_configs['appkey'] = self.appkey

        '''
        set sign_type,if is set
        '''
        if self.sign_type != '':
            mail_configs['sign_type'] = self.sign_type

        '''
        init mail class
        '''
        mail = Mail(mail_configs)

        '''
        build request and send email and return the result
        '''
        return mail.send(self.build_request())
