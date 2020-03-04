import { Box, Button, Card, Collapse, makeStyles, Typography } from '@material-ui/core';
import { observer } from 'mobx-react';
import React, { useEffect, useState } from 'react';
import ReactGA from 'react-ga';
import InfiniteScroll from 'react-infinite-scroller';
import { useParams } from 'react-router';
import ItemStore from 'store/item';
import ItemModel from 'store/item/model';

interface Params {
  id: string;
}

export const ItemList = observer(() => {
  const { id } = useParams<Params>();
  const [hasId, setHasId] = useState(!!id);

  useEffect(() => {
    if (!id) {
      return;
    }

    ItemStore.fetchById(id);
    setHasId(false);
  }, [id]);

  return hasId ? (
    <></>
  ) : (
    <InfiniteScroll
      loader={
        <div className="loader" key={0}>
          Loading ...
        </div>
      }
      loadMore={ItemStore.fetch}
      hasMore={!ItemStore.isLoading}
      key={0}
    >
      {ItemStore.itemList.map(item => (
        <Item data={item} key={item.id}></Item>
      ))}
    </InfiniteScroll>
  );
});

const itemStyles = makeStyles({
  box: {
    marginTop: '1rem',
  },
  card: {
    padding: '1rem',
  },
  contentBox: {
    overflow: 'hidden',
  },
  button: {
    width: '100%',
    marginTop: '1rem',
  },
});

interface Props {
  data: ItemModel;
  key: number;
}

export const Item = ({ data, key }: Props) => {
  const item = data;
  const style = itemStyles();

  const [expaneded, setExpaned] = useState(false);

  const link = () => {
    const copyText = (x: string) => {
      const el = document.createElement('textarea');
      el.value = x;
      el.setAttribute('readonly', '');
      el.style.position = 'absolute';
      el.style.left = '-9999px';
      document.body.appendChild(el);
      if (navigator.userAgent.match(/ipad|ipod|iphone/i)) {
        const range = document.createRange();
        range.selectNodeContents(el);
        const sel = window.getSelection();
        if (sel) {
          sel.removeAllRanges();
          sel.addRange(range);
          el.setSelectionRange(0, 999999);
        }
      } else {
        el.select();
      }
      document.execCommand('copy');
      document.body.removeChild(el);
    };
    copyText(window.location.host + '/' + item.id + '?utm_source=share');
    alert('링크가 복사되었습니다!');
  };

  return (
    <Box className={style.box}>
      <Card className={style.card}>
        <Collapse in={expaneded} collapsedHeight={500}>
          <Box className={style.contentBox}>
            <Box mb="0.5rem">
              <Typography variant="h6">{item.title}</Typography>
              <Button onClick={link}>링크 복사하기</Button>
            </Box>
            <Box dangerouslySetInnerHTML={{ __html: item.content }}></Box>
          </Box>
        </Collapse>
        <Collapse in={!expaneded} collapsedHeight={0}>
          <Box>
            <Button
              className={style.button}
              onClick={() => {
                setExpaned(true);
                data.read();
                ReactGA.pageview('/' + item.id);
              }}
            >
              펼치기
            </Button>
          </Box>
        </Collapse>
      </Card>
    </Box>
  );
};
