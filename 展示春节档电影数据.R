library(readxl)
library(ggplot2)
library(ggimage)
library(ggthemr)
library(ggthemes)
library(Cairo)


setwd('D:/爬虫/春节档')
data = read_excel('春节档电影统计数据.xlsx')
data$score = round(as.numeric(data$score),2)
data$sale=as.numeric(data$sale)
data$label_sale=paste(data$name,':',data$sale)
data$label_score=paste(data$name,':',data$score)
data$label_key=paste(data$name,':',data$key_words)

## 展示评价数据

p<-ggplot(data[order(data$score,decreasing = T),][1:8,],
          aes(x=reorder(name,score),y=score,fill=name))+
  geom_bar(stat='identity',width = 0.5)+
  geom_image(aes(x=name,y=0,image=image),size=0.08)+
  geom_text(aes(x=name,y=2,label=label_score),size = 7,col='black',fontface='bold')+
  ggtitle('春节档电影上映前评价') + theme_wsj()+ scale_fill_tableau()+                 
  theme(axis.text.x = element_blank(),
        axis.text.y = element_blank(),
        plot.title = element_text(hjust=0.5,size=30),
        panel.grid = element_blank(),
        legend.position = 'none',
        panel.background = element_blank(),
        axis.title  = element_blank(),
        axis.line = element_blank(),
        axis.ticks = element_blank()
  )+coord_flip()+ylim(0,5)
ggsave("春节档上映前评分排名.png", p, width = 8, height = 12)


## 展示预售数据

p<-ggplot(data[order(data$sale,decreasing = T),][1:8,],
          aes(x=reorder(name,sale),y=sale,fill=name))+
  geom_bar(stat='identity',width = 0.5)+
  geom_image(aes(x=name,y=0,image=image),size=0.08)+
  geom_text(aes(x=name,y=2500,label=label_sale),size = 7,col='black',fontface='bold')+
  ggtitle('春节档电影预售票房排名(万)') + theme_wsj()+ scale_fill_tableau()+                 
  theme(axis.text.x = element_blank(),
        axis.text.y = element_blank(),
        plot.title = element_text(hjust=0.5,size=30),
        panel.grid = element_blank(),
        legend.position = 'none',
        panel.background = element_blank(),
        axis.title  = element_blank(),
        axis.line = element_blank(),
        axis.ticks = element_blank()
  )+coord_flip()+ylim(0,6500)
ggsave("春节档上映前预售排名.png", p, width = 8, height = 12)


## 展示看点
data$film_num <- 0:7
data$image_pos_x = data$film_num%%2
data$image_pos_y = data$film_num%/%2
data$key_pos_x = data$film_num%%2+0.4
data$key_pos_y = data$film_num%/%2-0.2
data$name_pos_y = data$film_num%/%2+0.2


ggthemr('grape')
p<-ggplot(data,aes(x=image_pos_x,y=image_pos_y,fill=name))+
  geom_image(aes(image=image),size=0.15)+xlim(-0.1,1.7)+ylim(-0.5,3.5)+
  ggtitle('春节档电影看点') + theme_wsj()+ scale_fill_tableau()+ 
  geom_text(aes(x=key_pos_x,y=key_pos_y,label=key_words),size = 7,col='black',fontface='bold')+
  geom_text(aes(x=key_pos_x,y=name_pos_y,label=name),size = 7,col='black',fontface='bold')+
  theme(axis.text.x = element_blank(),
        axis.text.y = element_blank(),
        plot.title = element_text(hjust=0.5,size=30),
        panel.grid = element_blank(),
        legend.position = 'none',
        panel.background = element_blank(),
        axis.title  = element_blank(),
        axis.line = element_blank(),
        axis.ticks = element_blank()
  )
ggsave("春节档看点.png", p, width = 18, height = 8)
