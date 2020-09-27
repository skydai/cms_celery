# coding=utf-8
from __future__ import absolute_import, unicode_literals

from celery.task import Task
from celery.result import AsyncResult


class CreateInstanceCallbackTask(Task):
    def on_success(self, retval, task_id, args, kwargs):
        pass

    def on_failure(self, exc, task_id, args, kwargs, einfo):

        import json
        from cmsconfig import UPDATE_OPENSTACK_NODE
        from util.http_client import HttpClientUtil
        import logging

        logger = logging.getLogger(__name__)
        status = "FAILED"
        if args:
            nodes = args[0].get('nodes', "")
            instance_name = str(args[0].get('name', ""))
        else:
            nodes = []
            instance_name = ""

        try:

            print "url= " + str(UPDATE_OPENSTACK_NODE)
            print "data= " + str(json.dumps({"nodes": nodes, "status": status, "instance_name": instance_name}))

            HttpClientUtil.doPut(url=str(UPDATE_OPENSTACK_NODE), auth_token="",
                                 data=json.dumps({"nodes": nodes, "status": status, "instance_name": instance_name}))

        except Exception as e:
            logger.warn("PUT:  " + str(UPDATE_OPENSTACK_NODE) + " --data " + str(json.dumps({"nodes": nodes})) + " FAIL")

        import smtplib
        from email.mime.multipart import MIMEMultipart
        from email.mime.text import MIMEText
        fromaddr = "jenkins@transwarp.io"
        toaddr = str(args[0].get("email"))
        username = "jenkins@transwarp.io"
        password = "Or37aZ0ST7WV0fBj"
        res = AsyncResult(task_id)
        log_info = res.traceback
        # define msg header
        msg = MIMEMultipart('alternative')
        msg['Subject'] = "[CMS-Link]Sorry, Your task Failed, Please contact to the administrator youzhi.su@transwarp.io !"
        msg['From'] = fromaddr

        tolist = [x.strip() for x in toaddr.split(',')]
        if 'youzhi.su@transwarp.io' not in tolist:
            tolist.append('youzhi.su@transwarp.io')


        msg['To'] = ",".join(tolist)

        text = "Hi!\nHere is information about Cms-celery task\n"

        # define msg body
        html = """\
        <!doctype html>
        <html>
          <head>
            <meta name="viewport" content="width=device-width">
            <meta http-equiv="Content-Type" content="text/html; charset=UTF-8">
            <title>Simple Transactional Email</title>
            <style>
            /* -------------------------------------
                INLINED WITH htmlemail.io/inline
            ------------------------------------- */
            /* -------------------------------------
                RESPONSIVE AND MOBILE FRIENDLY STYLES
            ------------------------------------- */
            @media only screen and (max-width: 620px) {{
              table[class=body] h1 {{
                font-size: 28px !important;
                margin-bottom: 10px !important;
              }}
              table[class=body] p,
                    table[class=body] ul,
                    table[class=body] ol,
                    table[class=body] td,
                    table[class=body] span,
                    table[class=body] a {{
                font-size: 16px !important;
              }}
              table[class=body] .wrapper,
                    table[class=body] .article {{
                padding: 10px !important;
              }}
              table[class=body] .content {{
                padding: 0 !important;
              }}
              table[class=body] .container {{
                padding: 0 !important;
                width: 100% !important;
              }}
              table[class=body] .main {{
                border-left-width: 0 !important;
                border-radius: 0 !important;
                border-right-width: 0 !important;
              }}
              table[class=body] .btn table {{
                width: 100% !important;
              }}
              table[class=body] .btn a {{
                width: 100% !important;
              }}
              table[class=body] .img-responsive {{
                height: auto !important;
                max-width: 100% !important;
                width: auto !important;
              }}
            }}
            /* -------------------------------------
                PRESERVE THESE STYLES IN THE HEAD
            ------------------------------------- */
            @media all {{
              .ExternalClass {{
                width: 100%;
              }}
              .ExternalClass,
                    .ExternalClass p,
                    .ExternalClass span,
                    .ExternalClass font,
                    .ExternalClass td,
                    .ExternalClass div {{
                line-height: 100%;
              }}
              .apple-link a {{
                color: inherit !important;
                font-family: inherit !important;
                font-size: inherit !important;
                font-weight: inherit !important;
                line-height: inherit !important;
                text-decoration: none !important;
              }}
              .btn-primary table td:hover {{
                background-color: #34495e !important;
              }}
              .btn-primary a:hover {{
                background-color: #34495e !important;
                border-color: #34495e !important;
              }}
            }}
            </style>
          </head>
          <body class="" style="background-color: #f6f6f6; font-family: sans-serif; -webkit-font-smoothing: antialiased; font-size: 14px; line-height: 1.4; margin: 0; padding: 0; -ms-text-size-adjust: 100%; -webkit-text-size-adjust: 100%;">
            <table border="0" cellpadding="0" cellspacing="0" class="body" style="border-collapse: separate; mso-table-lspace: 0pt; mso-table-rspace: 0pt; width: 100%; background-color: #f6f6f6;">
              <tr>
                <td style="font-family: sans-serif; font-size: 14px; vertical-align: top;">&nbsp;</td>
                <td class="container" style="font-family: sans-serif; font-size: 14px; vertical-align: top; display: block; Margin: 0 auto; max-width: 580px; padding: 10px; width: 580px;">
                  <div class="content" style="box-sizing: border-box; display: block; Margin: 0 auto; max-width: 580px; padding: 10px;">

                    <!-- START CENTERED WHITE CONTAINER -->
                    <span class="preheader" style="color: transparent; display: none; height: 0; max-height: 0; max-width: 0; opacity: 0; overflow: hidden; mso-hide: all; visibility: hidden; width: 0;">Sorry, Your task failed, check in detailed log in /tmp/auto_web_install/auto_web_install.log or /opt/TDHAutoInstall/TDHAutoInstall.log and ask for admin</span>
                    <table class="main" style="border-collapse: separate; mso-table-lspace: 0pt; mso-table-rspace: 0pt; width: 100%; background: #ffffff; border-radius: 3px;">

                      <!-- START MAIN CONTENT AREA -->
                      <tr>
                        <td class="wrapper" style="font-family: sans-serif; font-size: 14px; vertical-align: top; box-sizing: border-box; padding: 20px;">
                          <table border="0" cellpadding="0" cellspacing="0" style="border-collapse: separate; mso-table-lspace: 0pt; mso-table-rspace: 0pt; width: 100%;">
                            <tr>
                              <td style="font-family: sans-serif; font-size: 14px; vertical-align: top;">
                                <p style="font-family: sans-serif; font-size: 14px; font-weight: normal; margin: 0; Margin-bottom: 15px;"><b>[Cms Cluster Install]</b><br>Task ID: {TaskID} failed!</p>
                                <p style="font-family: sans-serif; font-size: 14px; font-weight: normal; margin: 0; Margin-bottom: 15px;">{LogInfo}</p>


                                <table border="0" cellpadding="0" cellspacing="0" class="btn btn-primary" style="border-collapse: separate; mso-table-lspace: 0pt; mso-table-rspace: 0pt; width: 100%; box-sizing: border-box;">
                                  <tbody>
                                    <tr>
                                      <td align="left" style="font-family: sans-serif; font-size: 14px; vertical-align: top; padding-bottom: 15px;">
                                        <table border="0" cellpadding="0" cellspacing="0" style="border-collapse: separate; mso-table-lspace: 0pt; mso-table-rspace: 0pt; width: auto;">
                                          <tbody>
                                            <tr>
                                              <td style="font-family: sans-serif; font-size: 14px; vertical-align: top; background-color: #3498db; border-radius: 5px; text-align: center;"> <a href="mailto:zhiyang.dai@transwarp.io" target="_blank" style="display: inline-block; color: #ffffff; background-color: #3498db; border: solid 1px #3498db; border-radius: 5px; box-sizing: border-box; cursor: pointer; text-decoration: none; font-size: 14px; font-weight: bold; margin: 0; padding: 12px 25px; text-transform: capitalize; border-color: #3498db;">Call To Action</a> </td>
                                            </tr>
                                          </tbody>
                                        </table>
                                      </td>
                                    </tr>
                                  </tbody>
                                </table>
                                <p style="font-family: sans-serif; font-size: 14px; font-weight: normal; margin: 0; Margin-bottom: 15px;">Good luck! Hope it works.</p>
                              </td>
                            </tr>
                          </table>
                        </td>
                      </tr>

            <!-- END MAIN CONTENT AREA -->
            </table>
                    <div class="footer" style="clear: both; Margin-top: 10px; text-align: center; width: 100%;">
                      <table border="0" cellpadding="0" cellspacing="0" style="border-collapse: separate; mso-table-lspace: 0pt; mso-table-rspace: 0pt; width: 100%;">
                        <tr>
                          <td class="content-block" style="font-family: sans-serif; vertical-align: top; padding-bottom: 10px; padding-top: 10px; font-size: 12px; color: #999999; text-align: center;">
                            <span class="apple-link" style="color: #999999; font-size: 12px; text-align: center;">Transwarp</span>
                            <br>Call me to ask more information<a href="mailto:zhiyang.dai@transwarp.io" style="text-decoration: underline; color: #999999; font-size: 12px; text-align: center;"><b>GateWay</b></a>.
                          </td>
                        </tr>
                        <tr>
                          <td class="content-block powered-by" style="font-family: sans-serif; vertical-align: top; padding-bottom: 10px; padding-top: 10px; font-size: 12px; color: #999999; text-align: center;">
                            Powered by <a href="https://skydai.github.io" style="color: #999999; font-size: 12px; text-align: center; text-decoration: none;">zhiyang.dai</a>.
                          </td>
                        </tr>
                      </table>
                    </div>

                  </div>
                </td>
                <td style="font-family: sans-serif; font-size: 14px; vertical-align: top;">&nbsp;</td>
              </tr>
            </table>
          </body>
        </html>
        """
        # retval task_id args kwargs

        html = html.format(TaskID=task_id, LogInfo=log_info)
        # Record the MIME types of both parts - text/plain and text/html.
        part1 = MIMEText(text, 'plain')
        part2 = MIMEText(html, 'html')

        # attach parts into msg container
        msg.attach(part1)
        msg.attach(part2)

        try:
            server = smtplib.SMTP_SSL('smtp.exmail.qq.com', port=465)
            # open debug and print logs
            # server.set_debuglevel(1)
            print("--- Need Authentication ---")
            server.login(username, password)
            server.sendmail(fromaddr, tolist, msg.as_string())
            print("success")
        except Exception as e:
            tolist = ['youzhi.su@transwarp.io']
            server.sendmail(fromaddr, tolist, msg.as_string())

        server.quit()

