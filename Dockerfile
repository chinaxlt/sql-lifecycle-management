FROM saas-acr-sh-registry.cn-shanghai.cr.aliyuncs.com/saas-test/saas-test:sqless_base_v0.0.1

ADD ./ /home/admin/dbplatform/sqless

WORKDIR /home/admin/dbplatform/sqless

# 最后确保admin目录下文件权限
RUN chown -R admin:admin /home/admin

CMD [ "sh", "/home/admin/dbplatform/sqless/start.sh" ]