import pexpect,re,time


class GrinWallet():
     def __init__(self,password):
          self.password = password
          

     def terminal(self,params):
          command = 'grin-wallet ' + params
          child = pexpect.spawn(command)
          child.expect('Password:')
          child.sendline(self.password)
          child.expect(pexpect.EOF)
          result = child.before.decode('utf-8')
          return result

     def terminal_s(self,params,slatepack):
          command = 'grin-wallet ' + params
          child = pexpect.spawn(command)
          child.expect('Password:')
          child.sendline(self.password)
          child.expect('message:')
          child.sendline(slatepack)
          child.expect(pexpect.EOF)
          result = child.before.decode('utf-8')
          return result

     def info(self):
          result = self.terminal('info')
          
          total_pattern = re.compile(r'Confirmed Total.*(\d+\.\d+)')
          total = re.search(total_pattern,result).group(1)
          confirmation_pattern = re.compile(r'Awaiting Confirmation.*(\d+\.\d+)')
          confirmation = re.search(confirmation_pattern,result).group(1)
          finalization_pattern = re.compile(r'Awaiting Finalization.*(\d+\.\d+)')
          finalization = re.search(finalization_pattern,result).group(1)
          locked_pattern = re.compile(r'Locked by previous transaction.*(\d+\.\d+)')
          locked = re.search(locked_pattern,result).group(1)
          spendable_pattern = re.compile(r'Currently Spendable.*(\d+\.\d+)')
          spendable = re.search(spendable_pattern,result).group(1)

          return (total,confirmation,finalization,locked,spendable)

     def confirmed_total(self):
          return self.info()[0]

     def awaiting_confirmation(self):
          return self.info()[1]

     def awaiting_finalization(self):
          return self.info(2)

     def locked(self):
          return self.info(3)

     def currently_spendable(self):
          return self.info(4)

     def address(self):
          result = self.terminal('address')

          pattern = re.compile(r'grin.*')
          addr = re.search(pattern,result).group()
          return addr

     def cancel(self,id=0):
          stop = False
          trans_nums = ''
          if id:
               params = 'cancel -i ' + str(id)
               result = self.terminal(params)
               res = result.split('\n')[-2]
               return res
          while not stop:
               params = 'cancel -i ' + str(id)
               result = self.terminal(params)
               id += 1
               if "doesn't exist" in result:
                    stop = True
               if 'successfully' in result:
                    trans_nums += f'{id} '
          res = f'Transaction {trans_nums} canceled successfully!'
          return res
          
     def receive(self,slatepack):
          result = self.terminal_s('receive -m',slatepack)

          pattern = re.compile(r'/home.*?S2.slatepack')
          slate_file = re.search(pattern,result).group()
          with open(slate_file,'r') as f:
               slate = f.read()
          return slate

     def scan(self):
          child = pexpect.spawn('grin-wallet scan')
          child.expect('Password:')
          child.sendline(self.password)
          
     def send(self,amount):
          result = self.terminal('send ' + str(amount))
          pattern = re.compile(r'/home.*?S1.slatepack')
          slate_file = re.search(pattern, result).group()
          with open(slate_file,'r') as f:
               slatepack = f.read()
          return slatepack

     def finalize(self,slatepack):
          result = self.terminal_s('finalize',slatepack)
          return result
