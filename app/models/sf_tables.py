from sqlalchemy import Column, Integer, String, Boolean, ForeignKey
from app.db.base import Base

class TerritoryInfo(Base):
    __tablename__ = 'territory_info'
    
    territory_info_id = Column(Integer, primary_key=True)
    sfa_territory_id = Column(Integer, nullable=False)
    territory_code = Column(String(4), nullable=False)
    territory = Column(String(40), nullable=False)


class ChannelInfo(Base):
    __tablename__ = 'channel_info'
    
    channel_info_id = Column(Integer, primary_key=True)
    sfa_channel_id = Column(Integer, nullable=False)
    channel_code = Column(String(4), nullable=False)
    channel = Column(String(40), nullable=False)


class ChainInfo(Base):
    __tablename__ = 'chain_info'
    
    chain_info_id = Column(Integer, primary_key=True)
    sfa_chain_id = Column(Integer, nullable=False)
    chain_code = Column(String(4), nullable=False)
    chain_name = Column(String(40), nullable=False)


class BrandInfo(Base):
    __tablename__ = 'brand_info'
    
    brand_info_id = Column(Integer, primary_key=True)
    sfa_brand_id = Column(Integer, nullable=False)
    brand = Column(String(40), nullable=False)


class OutletInfo(Base):
    __tablename__ = 'outlet_info'
    
    outlet_info_id = Column(Integer, primary_key=True)
    sfa_outlet_id = Column(Integer, nullable=False)
    territory_info_id = Column(Integer, ForeignKey('territory_info.territory_info_id'))
    rt_code = Column(String(8))
    rt_name = Column(String(40))
    address_line1 = Column(String(40))
    address_line2 = Column(String(40))
    address_line3 = Column(String(40))
    address_line4 = Column(String(40))
    address_line5 = Column(String(40))
    channel_info_id = Column(Integer, ForeignKey('channel_info.channel_info_id'))
    brand_info_id = Column(Integer, ForeignKey('brand_info.brand_info_id'))
    is_chain = Column(Boolean)
    chain_info_id = Column(Integer, ForeignKey('chain_info.chain_info_id'))
    lat = Column(String(10))
    lng = Column(String(11))
